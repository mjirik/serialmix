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
        console.log(parseInt(event.target.getAttribute("name")))
        var channel= parseInt(event.target.getAttribute("name"))

        // alert("error");

        console.log("alkfdlskdf"+channel)
        var sliderDiv = document.getElementById("slider" + channel);
        sliderDiv.innerHTML = sliderAmount;
        // fetch("http://127.0.0.1:5000/send_message",
        fetch("http://localhost:5000/set_slider",
            {
                method: "POST",
                body: JSON.stringify({channel: channel, value: sliderAmount}),
                headers: {"content-type": "application/json"}
            }
        )
            .then(response => response.json())
            .then(data => console.log(data));
        console.log("ahoj")
        console.log(sliderAmount)
        console.log("za asyncem")

    }

    function restore_state(){
        var state = {}
        fetch("http://localhost:5000/get_state",
            {
                method: "POST",
                // body: JSON.stringify({channel: channel, value: sliderAmount}),
                // headers: {"content-type": "application/json"}
            }
        )
        .then(response => response.json())
        .then(
            data => {
                console.log("data")
                console.log(data)

                var sliders = document.getElementsByClassName("slider");
                for (const slider of sliders) {
                    // console.log(slider);
                    var channel = parseInt(slider.getAttribute("name"));
                    // console.log(channel);
                    slider.value = data[channel].value
                    // console.log()
                }

                console.log("Restoring buttons")
                var buttons = document.getElementsByClassName("btn");
                for (const button of buttons) {
                    // console.log(slider);
                    var channel = parseInt(button.getAttribute("name"));

                    console.log(channel);
                    console.log(button.id)
                    var room_id = parseInt(button.id[1])
                    var value = true
                    if (room_id==1){
                        value = data[channel].mute1
                    } else {
                        value = data[channel].mute2
                    }
                    console.log("value=" + value)
                    console.log(button.classList)

                    if (value) {
                        console.log("remove btn-succes")
                        // button.classList.remove("btn-sucess")
                    } else {
                        console.log("add btn-succes")
                        $(button).toggleClass('btn-success')
                        // button.classList.add("btn-sucess")
                    }

                    // slider.value = data[channel].value
                    // console.log()
                }
            }
        );

        var sliderDiv = document.getElementById("slider1");

        console.log("state restored")
    }

    function hasClass(element, className) {
        return (' ' + element.className + ' ').indexOf(' ' + className+ ' ') > -1;
    }

    $('.btn').click(function(e) {
        // $('.Button').not(this).removeClass('active');
        $(this).toggleClass('btn-success');
        e.preventDefault();
        console.log(this);
        var channel= parseInt(e.target.getAttribute("name"));
        // var muted = $(this).classList.contains("btn-sucess");
        var muted = true;
        muted = hasClass(this, "btn-success");

        var room_id = parseInt(this.id[1])
        console.log("muted=" + muted);
        console.log("channel=" + channel);
        console.log("id=" + room_id);

        fetch("http://localhost:5000/set_mute",
            {
                method: "POST",
                body: JSON.stringify({channel: channel, value: muted, room_id:room_id}),
                headers: {"content-type": "application/json"}
            }
        )
            .then(response => response.json())
            .then(data => console.log(data));
    });

    $('.Button').click(function(e) {
        // $('.Button').not(this).removeClass('active');
        $(this).toggleClass('active');
        e.preventDefault();
    });


    restore_state()
}
// Slider


