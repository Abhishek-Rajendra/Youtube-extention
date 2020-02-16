// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

'use strict';

// var span_notFound = document.getElementById('not-found');
// span_notFound.innerHTML = "";

var count_row=0;
var id;
var url;
chrome.tabs.query({'active': true, 'currentWindow': true}, function (tabs) {
  url = tabs[0].url;
  id = url.split('v=')[1]
});

  function runCommand(st) {
    // document.write(st)
    chrome.tabs.query({active: true, lastFocusedWindow: true}, function(tabs) {
      var url = tabs[0].url
      var index = url.lastIndexOf("#t")
      if(index>0)
        chrome.tabs.update(tabs[0].id, {url: url.substring(0,index) + "#t="+st});
      else
      chrome.tabs.update(tabs[0].id, {url: url + "#t="+st});


    });

  }

 function fetchya(word,id){
   
    // document.write(word+id)
    fetch('http://10.196.8.192:5000/'+ word +'/' + id).then(r => r.text()).then(result => {

      
      var mydata = JSON.parse(result);
      // document.write(mydata.length)
      var i;
      var x = [];

      var table = document.getElementById("tbody");


      if (mydata.length == 0) {
        var temp = document.getElementById('not-found')
        temp.innerHTML = "Word not found in Video, or very trivial. Please try another keyword!"
      }else{
        var span_notFound = document.getElementById('not-found');
      span_notFound.innerHTML = "";
      }

      

      for (var i = 1; i < mydata.length; i++) {
            
            var row = table.insertRow(-1);
            
            var cell2 = row.insertCell(-1);

            var index = mydata[i].phrase.indexOf(word);
            if (index >= 0) { 
              mydata[i].phrase = mydata[i].phrase.substring(0,index) +  "<mark>" + mydata[i].phrase.substring(index,index+word.length) + "</mark>" + mydata[i].phrase.substring(index + word.length);
              
            }
            cell2.innerHTML = ". . . " + mydata[i].phrase + " . . .";
            var cell = row.insertCell(-1);
            // var l = document.createElement("BUTTON");
            // l.setAttribute("id", mydata[i].timestamp)
            cell.innerHTML = "<input type = \"button\"  class = \"btn btn-info\" style = \"width: 100%;'font-family: \"Source Sans Pro\"; color: \"#ffffff\";\" id = \"" +  mydata[i].timestamp + "\" value = \"" + mydata[i].timestamp +"\" onclick = runCommand("+mydata[i].timestamp+"\">"
            document.getElementById(mydata[i].timestamp).addEventListener("click", function(e) {
              // alert(this.id)
              runCommand(this.id)
            });
            count_row++;
            
    }
    
    // for (var i = 1; i < mydata.length; i++) {
    //   document.getElementById(mydata[i].timestamp).addEventListener("click", function(e) {
    //     alert("pp")
    //     // runCommand(mydata[i].timestamp)
    //   }); 
    // }
      // for (i = 0; i < 2;i++){
      //   var row = table.insertRow(i);
      //   var cell1 = row.insertCell(0);
      //   var cell2 = row.insertCell(1);
      //   cell1.innerHTML = "mydata[i].timestamp";
      //   cell2.innerHTML = "mydata[i].phrase";
        // var l = document.createElement("BUTTON");
        // l.setAttribute("id", mydata[i].timestamp)
        // l.setAttribute("onclick", function() {
        //   // runCommand(l.getAttribute("id"))
        //   alert()
        // });
        // l.innerHTML = String(mydata[i].timestamp );//+ ' ' + mydata[i].phrase);
        //document.body.appendChild(row);
        //document.write(mydata[i].timestamp);
        
      // }
    //   for ( var i = 0; i < mydata.length; i++ ) (function(i){
    //     y = document.getElementById(mydata[i].timestamp);
    //     y.onclick = function() {
    //       runCommand(mydata[i].timestamp);
    //     }
    // })(i);
      // for (i = 0; i < 3;i++){
      //   //document.write(x.length)
      //   document.write(i)

      //
      // }
        //document.write(mydata[i].timestamp)
  //  alert(result)


      // Result now contains the response text, do what you want...

  });
  

  }

var word;
// var search = document.getElementById('submit')

// search.addEventListener('click', () => {
//   setTimeout(() => {
//     items.forEach(item => {
//       //your code here
//       alert("pp")
//       })
//   }, 2000)
// })

window.addEventListener('load', () => {
  document.getElementById('form').addEventListener('submit', function(evt) {
    evt.preventDefault();
    word=document.getElementById('word').value;

    var rowlength = $('#tbody tr').length;
    // alert(rowlength)
    for (var i=0; i<rowlength; i++) {
      
      document.getElementById("tbody").deleteRow(0);
      // alert( $('#tbody tr').length)
    }

    var span_notFound = document.getElementById('not-found');
      span_notFound.innerHTML = "Loading Results...";
    setTimeout(() => {
        //your code here
        // document.write(word)
        // document.querySelectorAll('#tbody').remove();
         
        fetchya(word,id)
        


    }, 1000)
  })
})

// search.onclick = function() {
//   word=document.getElementById('word').value;
//   // alert(word)
//   // document.write("")
//   // document.write(id)
//   // sleep(1000);
//   // alert('Hello');
//   fetchya(word,id);
  
// };
