
function data(){
    let first_name       = document.getElementById("FIRSTNAME").value
    let username         = document.getElementById("USERNAME").value
    let last_name        = document.getElementById("LASTNAME").value
    let age              = document.getElementById("AGE").value
    let email            = document.getElementById("EMAIL").value
    let gender           = document.getElementById("GENDER").value
    let phone            = document.getElementById("PHONENUMBER").value
    if(username==""||age=="" || email==""|| gender=="" || phone==""||first_name==""|| last_name==""){
        alert("All Fields are mendatory !");
        return false;
    }
    else if(isNaN(age)){
        alert("Only Number are allowed ! Please Enter Valid Age ");
        return false;
    }
    else if(age.lenght<2 || age.lenght>2){
        alert(" Plese Enter Valid AGE ");
        return false;
    }
    else if(phone.lenght<10||phone.lenght>10){
        alert("Number should be of 10 digits ! Plese Enter Valid Number ");
        return false;
    }
    else if(isNaN(phone)){
        alert("Only Number are allowed ! Please Enter Valid Number ");
        return false;
    }
    else if (gender=="__select__"){
      alert("please select age")
    }
   

   else{ 
  
           true;
   }
   
    

}
 