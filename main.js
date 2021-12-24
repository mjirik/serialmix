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

        var sliderDiv = document.getElementById("slider1");
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
            }
        );

        var sliderDiv = document.getElementById("slider1");

        console.log("state restored")
    }

    $('.btn').click(function(e) {
        // $('.Button').not(this).removeClass('active');
        $(this).toggleClass('btn-success');
        e.preventDefault();
    });

    $('.Button').click(function(e) {
        // $('.Button').not(this).removeClass('active');
        $(this).toggleClass('active');
        e.preventDefault();
    });


    restore_state()
}
// Slider


