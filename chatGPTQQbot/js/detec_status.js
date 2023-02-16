

try{
    var output_state_div = document.evaluate("//div[@class='relative flex h-full flex-1 md:flex-col']", document, null, XPathResult.ANY_TYPE, null).iterateNext().outerHTML;
    var gptstatus = "working";   
    if(true){
        if(output_state_div.includes("There was an error")){
            gptstatus = "error";
        }
        else if(output_state_div.includes(output_state_div.includes("</span>"))){
            gptstatus = "working";
        }
        
        else if(output_state_div.includes("</polygon>")){
            gptstatus = "finish";
        }
    }   
    console.log(gptstatus);
    return(gptstatus)
}catch(e){
    console.log("error");
    return("error")
}



