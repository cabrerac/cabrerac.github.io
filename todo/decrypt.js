/**
 * Decrypt task payload (PBKDF2 + AES-256-GCM).
 * Works in Node and in browser (Web Crypto API).
 * Payload format: JSON with { v, s, i, c } (version, salt, iv, ciphertext+tag in base64).
 *
 * Usage:
 *   const plaintext = await decrypt(payloadJsonString, password);
 *   // plaintext is the original tasks.yaml as UTF-8 string
 */

const PBKDF2_ITERATIONS = 100000;
const KEY_LENGTH = 32;
const GCM_AUTH_TAG_LENGTH = 16;
const SALT_LENGTH = 16;
const IV_LENGTH = 12;

function base64ToBytes(base64) {
  if (typeof Buffer !== 'undefined') {
    return Buffer.from(base64, 'base64');
  }
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

function bytesToBuffer(bytes) {
  if (typeof Buffer !== 'undefined') return Buffer.from(bytes);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

function bytesToBase64(bytes) {
  if (typeof Buffer !== 'undefined') return Buffer.from(bytes).toString('base64');
  let binary = '';
  const arr = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes);
  for (let i = 0; i < arr.length; i++) binary += String.fromCharCode(arr[i]);
  return btoa(binary);
}

/**
 * @param {string} payloadJsonString - JSON string of encrypted payload { v, s, i, c }
 * @param {string} password - User password
 * @returns {Promise<string>} - Decrypted plaintext (tasks.yaml content)
 */
async function decrypt(payloadJsonString, password) {
  const payload = JSON.parse(payloadJsonString);
  if (payload.v !== 1) throw new Error('Unsupported payload version');
  const salt = base64ToBytes(payload.s);
  const iv = base64ToBytes(payload.i);
  const c = base64ToBytes(payload.c);
  if (c.length < GCM_AUTH_TAG_LENGTH) throw new Error('Invalid payload');
  const tag = c.slice(-GCM_AUTH_TAG_LENGTH);
  const ciphertext = c.slice(0, -GCM_AUTH_TAG_LENGTH);

  if (typeof window !== 'undefined' && window.crypto && window.crypto.subtle) {
    return decryptBrowser(salt, iv, ciphertext, tag, password);
  }
  return decryptNode(salt, iv, ciphertext, tag, password);
}

async function decryptBrowser(salt, iv, ciphertext, tag, password) {
  const enc = new TextEncoder();
  const passwordKey = await crypto.subtle.importKey(
    'raw',
    enc.encode(password),
    'PBKDF2',
    false,
    ['deriveKey']
  );
  const key = await crypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt: salt,
      iterations: PBKDF2_ITERATIONS,
      hash: 'SHA-256',
    },
    passwordKey,
    { name: 'AES-GCM', length: 256 },
    false,
    ['decrypt']
  );
  const combined = new Uint8Array(ciphertext.length + tag.length);
  combined.set(ciphertext);
  combined.set(tag, ciphertext.length);
  const plain = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: iv, tagLength: 128 },
    key,
    combined
  );
  return new TextDecoder().decode(plain);
}

/**
 * Encrypt plaintext (browser only). Same format as diary encrypt script.
 * @param {string} plaintext - e.g. YAML string
 * @param {string} password
 * @returns {Promise<{ v: number, s: string, i: string, c: string }>}
 */
async function encrypt(plaintext, password) {
  if (typeof window === 'undefined' || !window.crypto || !window.crypto.subtle) throw new Error('Encrypt only available in browser');
  const enc = new TextEncoder();
  const salt = new Uint8Array(SALT_LENGTH);
  const iv = new Uint8Array(IV_LENGTH);
  crypto.getRandomValues(salt);
  crypto.getRandomValues(iv);
  const passwordKey = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']);
  const key = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: PBKDF2_ITERATIONS, hash: 'SHA-256' },
    passwordKey,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt']
  );
  const ctWithTag = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv, tagLength: 128 },
    key,
    enc.encode(plaintext)
  );
  return {
    v: 1,
    s: bytesToBase64(salt),
    i: bytesToBase64(iv),
    c: bytesToBase64(new Uint8Array(ctWithTag))
  };
}

function decryptNode(salt, iv, ciphertext, tag, password) {
  const crypto = require('crypto');
  const key = crypto.pbkdf2Sync(password, bytesToBuffer(salt), PBKDF2_ITERATIONS, KEY_LENGTH, 'sha256');
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, bytesToBuffer(iv));
  decipher.setAuthTag(bytesToBuffer(tag));
  const buf = Buffer.concat([decipher.update(bytesToBuffer(ciphertext)), decipher.final()]);
  return buf.toString('utf8');
}

// Export for Node and browser
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { decrypt, encrypt };
}
if (typeof self !== 'undefined') {
  self.TODO_decrypt = { decrypt, encrypt };
}
