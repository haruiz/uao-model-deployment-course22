

function sleepSync(ms) {
    var start = new Date().getTime()
    var expire = start + ms;
    while (new Date().getTime() < expire) { }
    return;
  }

  function sleepAsync(ms) {
    return new Promise(
        resolve => setTimeout(resolve, ms)
        );
}   

async function attatchNasaPictureToMyWebSite(){
    const url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY";
    const response = await fetch(url);
    const data = await response.json();
    const imageUri = data.url;
    const image = document.createElement("img");
    image.src = imageUri;
    image.width = 300;
    document.body.appendChild(image);
}


document.addEventListener("DOMContentLoaded", function() {

    
    const button = document.getElementById("btnRunModel");
    const terminal = document.getElementById("divTerminal");
    const buttonCallTest = document.getElementById("btnCallBlockingFunction");

    buttonCallTest.addEventListener("click", function() {
        sleepAsync(300000);
        terminal.innerHTML = "Blocking function called";
    });

    

    // this code is executed when the page is loaded
    // initialize terminal
    const cmd = "~ root$ Welcome to my website";
    appendCommand(cmd);
    console.log('ml5 version:', ml5.version);
    disabledButton();
    attatchNasaPictureToMyWebSite();
    
    // Initialize the Image Classifier method with MobileNet
    const classifier = ml5.imageClassifier('MobileNet', modelLoaded);

    // When the model is loaded
    function modelLoaded() {
        console.log('Model Loaded!');
        enabledButton();
    }

    // When the button is clicked
   function disabledButton() {
        button.disabled = true;
        button.innerHTML = "Loading model...";
    } 

    // When the button is clicked
    function enabledButton() {
        button.disabled = false;
        button.innerHTML = "Run Model";
    }

   function toggleConsole() {
        const visibility = terminal.style.visibility;
        if (visibility === "hidden") {
            terminal.style.visibility = "visible";
        } else {
            terminal.style.visibility = "hidden";
        }
    }
    
    function appendCommand(cmdText) {
        const cmdHtmlElement = document.createElement("p");
        cmdHtmlElement.innerHTML = cmdText;
        terminal.appendChild(cmdHtmlElement);
    }

    function clearTerminal() {
        terminal.innerHTML = ""; // clear the terminal div
    }

    button.addEventListener("click", async function() {
        //clearTerminal();
        //toggleConsole();
        try{
            const image = document.getElementById('mySiteImage');
            appendCommand("~ root$ Running model...");
            const results = await classifier.classify(image);
            console.log(results);
            results.forEach( prediction => {
                const cmd = "|-" + prediction.label + " " + prediction.confidence.toFixed(2);
                appendCommand(cmd);
            });


            // classifier.classify(image)
            // .then(results => {
            //     console.log(results);
            //     results.forEach( prediction => {
            //         const cmd = "|-" + prediction.label + " " + prediction.confidence.toFixed(2);
            //         appendCommand(cmd);
            //     });
            // })
            // .catch(err => {
            //     console.log(err);
            // });

        } catch (error) {
            console.log(error); // log error to console
        }
       
       
        // classifier.classify(image, (err, results) => {
        //     if(err){
        //         console.error("Something went wrong! : "+ err);
        //         return;
        //     }
        //     console.log(results);
        //     // processing the results
        //     results.forEach( prediction => {
        //         const cmd = "|-" + prediction.label + " " + prediction.confidence.toFixed(2);
        //         appendCommand(cmd);
        //     });
        // });
      

    });
});