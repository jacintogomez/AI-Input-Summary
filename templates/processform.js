document.querySelector('form').addEventListener('submit',async function(e){
    document.getElementById('loading-results').style.display='block';
    const formdata=new FormData(this);
    try{
        const response=await fetch('/process',{
            method:'POST',
            body:formdata
        });
        if(!response.ok){
            throw new Error('Server error: '+response.status);
        }
        const result=await response.json();
        document.getElementById('loading-results').style.display='none';
        document.getElementById('result').innerText=result;
    }catch(error){
        document.getElementById('loading-results').style.display='none';
        alert('Sorry, an error occurred: '+error.message);
    }
});