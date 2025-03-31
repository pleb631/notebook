function getUrl() {
    const identifier = document
        .querySelector("#unique-identifier")
        .nextElementSibling.innerText.split(".");
    const version =
        document.querySelector("#version").nextElementSibling.innerText;
    const vsix_url = `https://marketplace.visualstudio.com/_apis/public/gallery/publishers/${identifier[0]}/vsextensions/${identifier[1]}/${version}/vspackage`;
    console.log("下载地址", vsix_url);
}
getUrl();
