 script>
        document.getElementById('uploadForm').onsubmit = async function(e) {
            e.preventDefault();<
            let formData = new FormData();
            formData.append("video", document.getElementById("video").files[0]);
            
            document.getElementById("result").innerText = "Processing... Please wait.";

            try {
                let response = await fetch("http://localhost:5000/upload", {
                    method: "POST",
                    body: formData
                });
                let data = await response.json();
                document.getElementById("result").innerText = "Result: " + data.result;
            } catch (error) {
                document.getElementById("result").innerText = "Error processing video.";
            }
        }
    </script>
</body>
</html>
