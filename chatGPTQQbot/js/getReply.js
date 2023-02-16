//const { time } = require("console");

var elements = document.evaluate("(//div[@class='markdown prose w-full break-words dark:prose-invert dark'])[last()]", document, null, XPathResult.ANY_TYPE, null);
var element = elements.iterateNext();
var output = "";

var toomany_elements = document.evaluate("(//div[@class='w-full border-b border-black/10 dark:border-gray-900/50 text-gray-800 dark:text-gray-100 group bg-gray-50 dark:bg-[#444654]'])[last()]", document, null, XPathResult.ANY_TYPE, null);

try{
  if(toomany_elements.iterateNext().outerHTML.includes("Too many requests in 1 hour. Try again later")){
    return "😫你发送的次数太多啦，一小时之后再来吧"
  }
  if (element) {
    var children = element.children;
      for (var i = 0; i < children.length; i++) {
        if (children[i].tagName === "P") {
          output += children[i].outerHTML + "\n";
        } else if (children[i].tagName === "OL") {
          var listItems = children[i].getElementsByTagName("li");
            for (var j = 0; j < listItems.length; j++) {
            output += listItems[j].outerHTML + "\n";
            }
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