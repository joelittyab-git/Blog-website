window.addEventListener('load', function(){
    document.getElementById("tag-field").onclick = function(){
        const mediaQuery = window.matchMedia('(max-width: 1000px)');
        if(document.getElementById('tag-drop-down').style.visibility==='visible'){
            document.getElementById('tag-drop-down').style.visibility='hidden';
            if (mediaQuery.matches) {
                document.getElementById('overlay').style.visibility = 'hidden';
            }
        }else{
            if (mediaQuery.matches) {
                document.getElementById('overlay').style.visibility = 'visible';
            }
            document.getElementById('tag-drop-down').style.visibility = 'visible';
        }
    }


    

    var selectElement = document.getElementById("select-opt");
    var inputElement = document.getElementById("tag-field");

      // Add event listener to the select element
      selectElement.addEventListener("change", function () {
        // Get the selected options
        var selectedOptions = Array.from(selectElement.selectedOptions);

        // Get the selected option texts
        var selectedTexts = selectedOptions.map(function (option) {
          return option.text;
        });

        // Set the selected option texts as the value of the input element
        inputElement.value = selectedTexts.join(", ");

        if(inputElement.value == 'Others'){
            document.getElementById('others-entry').style.visibility = 'visible';
        }else{
            document.getElementById('others-entry').style.visibility = 'hidden';
        }
      });

      
    const userTagField = document.getElementById('user-tag-field');
    const topicTagField = document.getElementById('topic-tag-field');
    let word = "";
    var validPattern = /^[a-zA-Z0-9!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]+$/;
    let frmt_word = "";
    let arr = []
    
    

    userTagField.addEventListener('input',
        function(e){
            word = userTagField.value;

            if(word.endsWith(' ')){
                arr.push(word.split(' '));

                //Lopp to add '@' at the beggining of each user tag 
                arr = arr.map(function(element) {
                    if(!String(element).charAt(0) === '@'){
                        return '@' + element;
                    }else{
                        return element
                    }
                  });

                console.log(arr.join(' '));



                userTagField.value = arr.join(" ");

            }
        }
    )

    const setBoldText = this.document.getElementById('bold-text-ctnt');
    const content_field = this.document.getElementById('editable');

    setBoldText.addEventListener(
        "click",
        function(e) {
            content_field.style.fontWeight = "bold";
        }
    );
});

