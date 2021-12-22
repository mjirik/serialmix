window.onload=()=>{
    console.log(this)
    document.getElementById("slider1").addEventListener("change", (e) => {
        updateSlider(e)
        console.log(e)

    })

    function updateSlider(event)
    {
        var sliderAmount = event.target.value
        console.log(parseInt(event.target.getAttribute("name")))
        var cisloPosuvniku = parseInt(event.target.getAttribute("name"))

        // alert("error");

        var sliderDiv = document.getElementById("slider1");
        sliderDiv.innerHTML = sliderAmount;
        // fetch("http://127.0.0.1:5000/send_message",
        fetch("http://localhost:5000/send_message",
            {
                method: "POST",
                body: JSON.stringify({bla: 'bla', }),
                headers: {"content-type": "application/json"}
            }
        )
            .then(response => response.json())
            .then(data => console.log(data));
        // .then(response_json => {
        //     console.log(response_json)
        //     }
        // )
        console.log("ahoj")
        console.log(sliderAmount)
        // const xhr = new XMLHttpRequest();
        //     sender = JSON.stringify([
        //    [1, 2, 3],
        //    [4, 5, 6],
        //    [7, 8, 9]
        // ])
        // xhr.open('POST', "http://127.0.0.1:5000/send_message");
        // xhr.send(sender);
        // fetch('http://localhost:8088/api/login', {
        //     username: authData.username,
        //     password: authData.password
        // }, {
        //     mode: 'no-cors',
        //     method: 'post',
        //     url: `http://localhost:8088`,
        //     credentials: 'include'
        // })

        // async () => {
        //
        //     // data = {
        //     //     "id": 0,
        //     //     "message"
        //     // }
        //
        //     const response = await fetch('http://127.0.0.1:5000/send_message', {method: "POST"});
        //     const myJson = await response.json(); //extract JSON from the http response
        //     console.log("konstanty nastaveny")
        //     // do something with myJson
        // }
        console.log("za asyncem")

    }
    function createMessage(slider_id, )
    {
        message = "SET"

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
}
// Slider


