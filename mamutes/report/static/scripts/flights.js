// const submitCancelBotao = document.querySelector(".submitCancelBotao");
//     const modalFilter = document.querySelector(".modalFilter");
//     const closeModalBtn = document.getElementById("closeModalBtn");

//     modalFilter.style.display = "none";

//     submitCancelBotao.addEventListener("click", function () {
//         const isVisible = modalFilter.style.display === "flex";

//         modalFilter.style.display = isVisible ? "none" : "flex";
//         submitCancelBotao.classList.toggle("active", !isVisible);
//     });

//     closeModalBtn.addEventListener("click", function () {
//         modalFilter.style.display = "none";
//         submitCancelBotao.classList.remove("active");
//     });

// // document.addEventListener("click", (e) => {
// //     let target = e.target;

// //     if (target.classList.contains("btns")) {
// //         alert('MAUARA')
// //         let modal = document.querySelector(".modal");                        
// //         // if (!modalPrime.modalHTML) {
// //         //     modalPrime.modalHTML = modal.innerHTML;
// //         // }      
// //         if (modal) {
// //             modal.showModal();
// //             alert('OLA')
// //         }
// //         alert('OI MUNDO')
// //     }
// // })


// // Função para abrir o modal correto
// // function openModal(modalId) {
// //     document.getElementById(modalId).style.display = "flex";
// // }

// // // Função para fechar o modal correto
// // function closeModal(modalId) {
// //     document.getElementById(modalId).style.display = "none";
// // }

// // // Adiciona eventos de clique para abrir os modais
// // document.getElementById("modalNewFlight").addEventListener("click", function () {
// //     openModal("modalNewFlight");
// // });

// // document.getElementById("modalViewFlight").addEventListener("click", function () {
// //     openModal("modalViewFlight");
// // });

// // // Adiciona eventos para fechar os modais ao clicar no botão de fechar
// // document.querySelectorAll("closeModalBtn").forEach(btn => {
// //     btn.addEventListener("click", function () {
// //         closeModal(this.getAttribute("data-modal"));
// //     });
// // });

// // // Fecha o modal ao clicar fora da caixa
// // window.addEventListener("click", function (event) {
// //     document.querySelectorAll(".modal").forEach(modal => {
// //         if (event.target === modal) {
// //             modal.style.display = "none";
// //         }
// //     });
// // });
 
// // abrir modal novo flight
// document.addEventListener("DOMContentLoaded", function () {

//     const openModalBtn = document.getElementById("openModalBtn");
//     const modal = document.getElementById("modalNewFlight");
//     const closeModalBtn = document.getElementById("closeModalBtnNew");

//     openModalBtn.addEventListener("click", function () {
//         modal.style.display = "block";
//     });

//     closeModalBtn.addEventListener("click", function () {
//         modal.style.display = "none";
//     });

//     window.addEventListener("click", function (event) {
//         if (event.target === modal) {
//             modal.style.display = "none";
//         }
//     });

    



//     // window.addEventListener("click", function (event) {
//     //     if (event.target === modal) {
//     //         modalView.style.display = "none";
//     //     }
//     // });
// })

// // rating de voo
// document.addEventListener("DOMContentLoaded", function () {
//     const stars = document.querySelectorAll(".star");
//     const ratingText = document.getElementById("ratingText");

//     const ratings = ["Ruim", "Regular", "Bom", "Muito Bom", "Ótimo"];

//     stars.forEach((star, index) => {
//         star.addEventListener("click", function () {
//             let selectedValue = this.getAttribute("data-value");

//             stars.forEach((s, i) => {
//                 if (i < selectedValue) {
//                     s.classList.add("selected");
//                 } else {
//                     s.classList.remove("selected");
//                 }
//             });

//             ratingText.textContent = ratings[selectedValue - 1];
//         });
//     });
// });

// // mostra div adcional se checkbox marcado
// document.addEventListener("DOMContentLoaded", function () {
//     const checkbox = document.getElementById("accidentCheckbox");
//     const extraContent = document.getElementById("additionalInputs");

//     checkbox.addEventListener("change", function () {
//         if (this.checked) {
//             extraContent.classList.remove("accidentBox");
//         } else {
//             extraContent.classList.add("accidentBox");
//         }
//     });
// });

// // estilização para dropdown
// function showOptions(e) {
//     let divOptions = document.getElementById("divOptions");
//     if (divOptions.style.display == "none" || divOptions.style.display == "") {
//         divOptions.style.display = "inline-block";
//     } else {
//         divOptions.style.display = "none";
//     }
// }
// function clickMe(e) {
//     console.log('click me');
//     e.stopPropagation();
// }
// function hideOptions(e) {
//     let divOptions = document.getElementById("divOptions");

//     if (divOptions.contains(e.target)) {
//         divOptions.style.display = "inline-block";
//     } else {
//         divOptions.style.display = "none";
//     }
// }

// document.addEventListener("DOMContentLoaded", function () {
//     let checkbox = document.querySelectorAll("#divOptions input");
//     let inputCheckbox = document.getElementById("inputCheckbox");

//     for (let i = 0; i < checkbox.length; i++) {
//         checkbox[i].addEventListener("change", (e) => {
//             if (e.target.checked == true) {
//                 if (inputCheckbox.value == "") {
//                     inputCheckbox.value = checkbox[i].value;
//                 } else {
//                     inputCheckbox.value += `,${checkbox[i].value}`;
//                 }
//             } else {
//                 let values = inputCheckbox.value.split(",");

//                 for (let r = 0; r < values.length; r++) {
//                     if (values[r] == e.target.value) {
//                         values.splice(r, 1);
//                     }
//                 }
//                 inputCheckbox.value = values;
//             }
//         });
//     }
// });


const openModalBtns = document.querySelectorAll(".flightCard");
const modalViewFlights = document.querySelectorAll(".modalEditFlight"); // Corrigido para selecionar todos os modais

openModalBtns.forEach((btn) => {
    const modal = btn.querySelector(".modalEditFlight"); // Pegando o modal dentro do flightCard

    if (!modal) return; // Se não houver modal, pula para o próximo

    btn.addEventListener("click", function () {
        modal.style.display = "block";
    });

    const closeModalViewBtns = modal.querySelectorAll(".closeModalBtnEditFlight"); // Pegando os botões de fechar dentro do modal
    console.log(closeModalViewBtns)
    closeModalViewBtns.forEach((closeBtn) => {
        closeBtn.addEventListener("click", (event)=> {
            alert("fecha poha")
            const target = event.target;
            const modalOri = target.closest('.modalEditFlight');

            if(modalOri.style.display == "block"){
                modalOri.style.display = "none"; // Fecha apenas o modal correspondente
            }

        });
    });
});
        
