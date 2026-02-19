// Resume Upload
let resumeForm = document.getElementById("resumeForm");

if(resumeForm){
    resumeForm.addEventListener("submit", async function(e){

        e.preventDefault();

        let formData = new FormData(this);

        let res = await fetch("http://127.0.0.1:5000/upload_resume",{
            method:"POST",
            body:formData
        });

        let data = await res.json();

        // Make sure HTML has <p id="msg"></p>
        document.getElementById("msg").innerText = data.msg || data.error;
    });
}



// Job Upload
let jobForm = document.getElementById("jobForm");

if(jobForm){
    jobForm.addEventListener("submit", async function(e){

        e.preventDefault();

        let formData = new FormData(this);

        let res = await fetch("http://127.0.0.1:5000/upload_job",{
            method:"POST",
            body:formData
        });

        let data = await res.json();

        // Fix ID case
        document.getElementById("jobMsg").innerText = data.msg || data.error;
    });
}

