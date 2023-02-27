//const { time } = require("console");

var elements = document.evaluate("(//div[@class='markdown prose w-full break-words dark:prose-invert dark'])[last()]", document, null, XPathResult.ANY_TYPE, null);
var element = elements.iterateNext();
var childElements = element.querySelectorAll('p, pre, ol > li,table');
var output = "";

var toomany_elements = document.evaluate("(//div[@class='w-full border-b border-black/10 dark:border-gray-900/50 text-gray-800 dark:text-gray-100 group bg-gray-50 dark:bg-[#444654]'])[last()]", document, null, XPathResult.ANY_TYPE, null);

try{
  if(toomany_elements.iterateNext().outerHTML.includes("Too many requests in 1 hour. Try again later")){
    return "😫你发送的次数太多啦，一小时之后再来吧"
  }
  if (element) {
    for (let i = 0; i < childElements.length; i++) {
        if (childElements[i].tagName === 'TABLE') {
            var trElements = childElements[i].querySelectorAll('tr');
            

            for (let j = 0; j < trElements.length; j++) {
                var thElements = trElements[j].querySelectorAll('th, td');
                var thoutput = ""
                for(let n = 0; n < thElements.length; n++){
                    thoutput += (thElements[n].textContent + "\t|\t").toString();
                }
                output += thoutput + "\n";
            }
        }

         else {
            output += childElements[i].textContent + "\n";
        }
      }
  }
  return output;
}catch(e){
  return "🤦‍♀️GPT出现错误，请刷新网页或者查看后台🤦‍♂️"
}


// var blob = new Blob([output], {type: "text/plain"});
// var a = document.createElement("a");
// a.href = URL.createObjectURL(blob);
// a.download = "GPT.txt";

// // Create a hidden link and simulate a click to trigger the download
// a.style.display = "none";
// document.body.appendChild(a);
// a.click();

// // Remove the link from the DOM
// document.body.removeChild(a);

// // Save the file to the specified location on the E: drive
// var file = new File([blob], "GPT.txt", {type: "text/plain", lastModified: Date.now()});
// var fileReader = new FileReader();
// fileReader.onload = function() {
//   var content = fileReader.result;
//   var request = new XMLHttpRequest();
//   request.open("PUT", "file:///E:/GPT.txt", true);
//   request.send(content);
// };
// fileReader.readAsArrayBuffer(file);
// //console.clear();