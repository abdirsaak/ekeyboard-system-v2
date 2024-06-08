


    // ............... edit f_name model 


    let edi_f_name_tBtn = document.querySelector(".edi_f_name_tBtn")
    let Fn_editModal = document.querySelector("#Fn_editModal")
    let closeEditModal = document.querySelector("#closeEditModal")

    const displa_f_name_edit_model = () => {
        Fn_editModal.classList.toggle("hidden")
    }

    edi_f_name_tBtn.addEventListener("click", displa_f_name_edit_model)
    closeEditModal.addEventListener("click", () =>{
        Fn_editModal.classList.add("hidden")
    })


    

