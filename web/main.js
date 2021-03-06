window.onload=()=>{
    console.log(this)
    // document.getElementById("slider1").addEventListener("change", (e) => {
    //     updateSlider(e)
    //     console.log(e)
    // })
    var sliders = document.getElementsByClassName("slider")
    console.log("sliders")
    console.log(sliders)
    for (const slider of sliders) {
        slider.addEventListener("change", (e) => {
            updateSlider(e);
            console.log("slider update hook");
            console.log(e);
        });
    }

    function updateSlider(event)
    {
        var sliderAmount = event.target.value
        // console.log(parseInt(event.target.getAttribute("name")))
        var channel= parseInt(event.target.getAttribute("name"))

        // alert("error");

        console.log("update fader channel="+channel)
        var theValue = document.getElementById("slider-value" + channel);
        theValue.textContent=sliderAmount;



        var sliderDiv = document.getElementById("slider" + channel);
        sliderDiv.innerHTML = sliderAmount;
        // fetch("http://127.0.0.1:5000/send_message",
        var hostname = "localhost"
        if (window.location.hostname.length > 0) {
            hostname = window.location.hostname
        }
        // console.log(typeof window.location.hostname)
        var url = "http://" + hostname + ":5000/set_slider"
        var body = JSON.stringify({channel: channel, value: sliderAmount})
        console.log(url)
        console.log(body)
        fetch(url,
            {
                method: "POST",
                body: body,
                headers: {"content-type": "application/json"}
            }
        )
            .then(response => response.json())
            .then(error_data => {
                checkError(error_data);
                // console.log(error_data);
                // if (error_data.error) {
                //     showErrorMessage()
                //     console.error(data.message)
                // }
            });
        // console.log(sliderAmount)

    }

    function restore_state(){
        var state = {}
        var hostname = "localhost"
        if (window.location.hostname.length > 0) {
            hostname = window.location.hostname
        }
        fetch("http://" + hostname + ":5000/get_state",
            {
                method: "POST",
                // body: JSON.stringify({channel: channel, value: sliderAmount}),
                // headers: {"content-type": "application/json"}
            }
        )
        .then(response => response.json())
        .then(
            response_data => {
                var data = response_data.state
                var error_data = response_data.error
                checkError(error_data);
                console.log("Data from the REST API")
                console.log(data)

                console.log("Restoring the faders...")
                var sliders = document.getElementsByClassName("slider");
                for (const slider of sliders) {
                    // console.log(slider);
                    var channel = parseInt(slider.getAttribute("name"));
                    // console.log(channel);
                    slider.value = data[channel].value
                    // console.log()
                    var theValue = document.getElementById("slider-value" + channel);
                    theValue.textContent=data[channel].value;
                }

                console.log("Restoring the buttons...")
                var buttons = document.getElementsByClassName("button-slider");
                for (const button of buttons) {
                    // console.log(slider);
                    var channel = parseInt(button.getAttribute("name"));

                    console.log("channel=" + channel + " id=" + button.id);
                    var room_id = parseInt(button.id[1])
                    var value = true
                    if (room_id==1){
                        value = data[channel].mute1
                    } else {
                        value = data[channel].mute2
                    }
                    console.log("value=" + value)
                    // console.log(button.classList)

                    // to swap colors move toggle class to other if-part
                    if (value) {
                        console.log("remove btn-succes")
                        $(button).toggleClass('btn-success')
                    } else {
                        console.log("add btn-succes")
                    }
                }
            }
        );

        var sliderDiv = document.getElementById("slider1");

        console.log("state restored")
    }
    function checkError(error_data){
        if (error_data.error) {
            showErrorMessage();
            console.error(error_data.message);
        }
    }
    function showErrorMessage(){
        var theDiv = document.getElementById("error-container");
        if (hasClass(theDiv, "alert")) {

        } else {
            $(theDiv).toggleClass('alert');
            $(theDiv).toggleClass('alert-danger');
        }
        // console.log(theDiv)
        content = "Serial connection between the mixing console and the webserver lost. Check the hardware and refresh the page.<br>"
        // var content = document.createTextNode("malsdkfjal");
        theDiv.innerHTML += content;
    }

    function hasClass(element, className) {
        return (' ' + element.className + ' ').indexOf(' ' + className+ ' ') > -1;
    }

    $('.button-slider').click(function(e) {
        // $('.Button').not(this).removeClass('active');
        $(this).toggleClass('btn-success');
        e.preventDefault();
        // console.log(this);
        var channel= parseInt(e.target.getAttribute("name"));
        // var muted = $(this).classList.contains("btn-sucess");
        var muted = true;
        // to swap color remove !
        muted = !hasClass(this, "btn-success");

        var room_id = parseInt(this.id[1])
        console.log("muted=" + muted + " channel=" + channel + " room=" + room_id);

        var hostname = "localhost"
        if (window.location.hostname.length > 0) {
            hostname = window.location.hostname
        }
        fetch("http://" + hostname + ":5000/set_mute",
            {
                method: "POST",
                body: JSON.stringify({channel: channel, value: muted, room_id:room_id}),
                headers: {"content-type": "application/json"}
            }
        )
            .then(response => response.json())
            .then(error_data => {
                checkError(error_data);
            });
    });

    $('.button-projector').click(function(e) {
        // $('.Button').not(this).removeClass('active');
        // $(this).toggleClass('btn-success');
        e.preventDefault();
        // console.log(this);
        // var channel= parseInt(e.target.getAttribute("name"));
        // var muted = $(this).classList.contains("btn-sucess");
        // var muted = true;
        // to swap color remove !
        // muted = !hasClass(this, "btn-success");

        // var projector_button_id = parseInt(this.id[1])
        // console.log("muted=" + muted);
        // console.log("channel=" + channel);
        // console.log("id=" + projector_button_id);

        var hostname = "localhost"
        if (window.location.hostname.length > 0) {
            hostname = window.location.hostname
        }
        fetch("http://" + hostname + ":5000/projector",
            {
                method: "POST",
                body: JSON.stringify({id:this.id}),
                headers: {"content-type": "application/json"}
            }
        )
            .then(response => response.json())
            .then(error_data => {
                checkError(error_data);
            });
    });

    $('.Button').click(function(e) {
        // $('.Button').not(this).removeClass('active');
        $(this).toggleClass('active');
        e.preventDefault();
    });

    const input = document.querySelector("input");

    function setBackgroundSize(input) {
      input.style.setProperty("--background-size", `${getBackgroundSize(input)}%`);
    }

    setBackgroundSize(input);

    input.addEventListener("input", () => setBackgroundSize(input));

    function getBackgroundSize(input) {
        const min = +input.min || 0;
      const max = +input.max || 100;
      const value = +input.value;

      const size = (value - min) / (max - min) * 100;

      return size;
    }

    function updateValue(newValue){    document.getElementById("slider-value1").innerHTML = newValue ;
    }



    restore_state()
}
// Slider


