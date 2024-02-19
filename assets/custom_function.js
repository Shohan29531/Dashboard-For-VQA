

// document.addEventListener('DOMContentLoaded', function() {
//     setTimeout(function () {
//         var dropdown = document.querySelectorAll('#I-see .');
//
//         console.log(dropdown);
//         dropdown.addEventListener('change', function() {
//             console.log("sss");
//             var spans = document.querySelectorAll('#I-see .Select-value-label');
//             alert(spans);
//             // Apply red color to all selected options
//             // Array.from(dropdown.selectedOptions).forEach(function(option) {
//             //     alert(option.value);
//             //     option.style.color = 'red';
//             // });
//         });
//
//     }, 2000);
//
// });

// function change_color(){
//     var dropdown = document.querySelectorAll('#I-see .');
//
//     console.log(dropdown);
//     dropdown.addEventListener('change', function() {
//         console.log("sss");
//         var spans = document.querySelectorAll('#I-see .Select-value-label');
//         alert(spans);
//         // Apply red color to all selected options
//         // Array.from(dropdown.selectedOptions).forEach(function(option) {
//         //     alert(option.value);
//         //     option.style.color = 'red';
//         // });
//     });
// }

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    myNamespace: {
        customFunction: function() {
            // Your custom JavaScript code here
            // console.log('Custom function called with argument: ');
            // return 'Result from customFunction: ';
            var spans = document.querySelectorAll('#I-see .Select-value-label');
            // var span_divs = document.querySelectorAll('#I-see .Select-value-label');
            for (var i = 0; i < spans.length; i++) {
                if(spans[i].innerText.startsWith('+')){
                    spans[i].style.color = 'green';
                    // span_divs[i].style.border_color = 'green'
                }
                else{
                    spans[i].style.color = 'red';
                }
            }
        }
    }
});