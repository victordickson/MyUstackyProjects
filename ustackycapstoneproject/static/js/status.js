function setStatus(id){
	let status = document.getElementById('status').value;
  if(status === "admitted"){
    let url = `/admin/students/${id}/admitted`;
    fetch(url,{method:'POST'})
    .then(res=>res.text())
    .catch(err=>console.error(err))
    .then(state=>{
      if(state === "success"){
        window.alert("Student admitted successfully");
        let obj = document.getElementsByClassName("status");
        for(let i=0;i<obj.length;i++){
          obj[i].innerText = "admitted";
        }
      }
      else{
        window.alert("Error admitting student");
      }
    })
    .catch(err=>console.error(err))
  }

}