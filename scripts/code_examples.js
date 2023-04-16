const codeExamples = document.getElementsByClassName("code_examples")[0];
const exampleButtons = document.getElementsByClassName("code_example_buttons")[0];


function hideExamples(){
    for (let i = 0; i < codeExamples.children.length; i++) {
        codeExamples.children[i].style.display = "none";
        exampleButtons.children[i].style.backgroundColor = "#7e57c2";
        exampleButtons.children[i].style.animation = "";
    }
}


function changeExample(container, codeSwitchButton){
    const badCode = container.children[0];
    const goodCode = container.children[1];

    let visibleCode;
    let isGoodCode;
    let hiddenCode;

    if (badCode.style.display === "none" || container.style.display === "none") {
        hiddenCode = goodCode;
        visibleCode = badCode;
        isGoodCode = true;
        document.getElementsByClassName("overlay")[0].style.display = "inherit";
    } else {
        hiddenCode = badCode;
        visibleCode = goodCode;
        isGoodCode = false;
        document.getElementsByClassName("overlay")[0].style.display = "none";
    }

    hideExamples();
    hiddenCode.style.display = "none";
    visibleCode.style.display = "inherit";
    container.style.display = "inherit";

    const title = document.getElementById("code-comparison");

    if(isGoodCode){
        codeSwitchButton.style.backgroundColor = "#e6695b";
        codeSwitchButton.style.animation = "pulse 3s infinite";
        title.innerText = "Bad Code! Press again to refactor!"
    }else{
        codeSwitchButton.style.backgroundColor = "#2fb170";
        codeSwitchButton.style.animation = "";
        title.innerText = "PyAssimilator Code!"
    }
}


for (let currentIndex = 0; currentIndex < codeExamples.children.length; currentIndex++) {
    const currentExampleContainer = codeExamples.children[currentIndex];
    const codeSwitchButton = exampleButtons.children[currentIndex];

    codeSwitchButton.addEventListener("click", () => {
        changeExample(currentExampleContainer, codeSwitchButton);
    });
}


changeExample(codeExamples.children[0], exampleButtons.children[0]);
