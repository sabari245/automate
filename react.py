import sys
import subprocess

INJECT_SCRIPT = '''
<script>
  function imgMod() {
    let images = document.querySelectorAll("img");
    images.forEach((e) => {
      console.log(e.src);
      e.src =
        "./" +
        e.src.slice(e.src.indexOf("/static") + 1, e.src.length);
    });
  }
  setTimeout(function () {
    imgMod();
  }, 2000);

  // make a mutation observer
  let observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      setTimeout(function () {
        imgMod();
      }, 2000);
    });
  });
</script>
'''

try:
    directory = sys.argv[sys.argv.index("-d") + 1]
except:
    print("Please specify a directory with -d")
    sys.exit(1)

# to run the react build command
subprocess.call(f"cd \"{directory}\" && npm run build", shell=True)

# remove the old docs folder
subprocess.call(f"cd \"{directory}\" && rmdir /s /q  docs", shell=True)

# copy the build folder and rename it to docs
subprocess.call(
    f"Xcopy \"{directory}\\build\" \"{directory}\\docs\" /E /H /C /I", shell=True)

# rename the index.html file to index.md
subprocess.call(
    f"cd \"{directory}\\docs\" && rename index.html index.md", shell=True)

with open(f"{directory}\\docs\\index.md", "r") as f:
    with open(f"{directory}\\docs\\index.html", "w") as f2:
        content = f.read()
        content = content.replace("href=\"/", "href=\"")
        content = content.replace("src=\"/", "src=\"")
        content = content[:content.index(
            "</body>")] + INJECT_SCRIPT + content[content.index("</body>"):]
        f2.write(content)

print(sys.argv)
