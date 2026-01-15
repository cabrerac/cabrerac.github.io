(() => {
  const script = document.currentScript;
  const indexUrl = script?.dataset?.indexUrl;

  async function main() {
    const pyodide = await loadPyodide(
      indexUrl ? { indexURL: indexUrl } : undefined
    );
    await pyodide.loadPackage("numpy");
    await pyodide.loadPackage("matplotlib");
  }

  if (typeof loadPyodide === "function") {
    void main();
  } else {
    console.warn("Pyodide is not available on this page.");
  }
})();
