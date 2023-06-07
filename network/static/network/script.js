   function likes(id,myLikes) {
            const like = document.getElementById(`but_${id}`)
            if(myLikes.indexOf(id) >=0){
                var liked = true;
            }else{
                var liked = false;

            }

            if (liked){
            fetch(`/like/${id}/${0}`)
                .then(response => response.json())
                .then(result=> {
                                    like.style.color = "gray"

                })
            }else {
                fetch(`/like/${id}/${1}`)
                .then(response => response.json())
                .then(result=> {
                                    like.style.color = "darkred"

                })
            }
            liked != liked

    }

    function getCookie(name){
        const value =  `; ${document.cookie}`
        const parts = value.split(`; ${name}=`)
        if(parts.length==2) return parts.pop().split(';').shift()
    }
    function submit(id){
        const content = document.getElementById(`content_${id}`)
        const textarea = document.getElementById(`textarea_${id}`)
        fetch(`/edit/${id}`,{
            method:"POST",
            headers: {"Content-type":"application/json","X-CSRFToken":getCookie("csrftoken")},
            body: JSON.stringify({content: textarea.value})
        })
        .then(response => response.json())
        .then(result =>{
            console.log(result.data)
        content.innerHTML = result.data})
    }