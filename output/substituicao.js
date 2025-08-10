// Script para garantir que o título e a introdução sejam substituídos
window.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
    // Encontrar o elemento h1 com "Transformação Digital" e substituir
    var h1Elements = document.querySelectorAll("h1");
    for (var i = 0; i < h1Elements.length; i++) {
      if (h1Elements[i].textContent.includes("Transformação Digital para")) {
        console.log("Substituindo o título...");
        // Preserva o span com gradient-text se existir
        var spanElement = h1Elements[i].querySelector(".gradient-text");
        if (spanElement) {
          var clientName = spanElement.textContent;
          h1Elements[i].innerHTML = "Transformação digital de criação de proposta para novos clientes que vamos entrar em contato. <span class=\"gradient-text\">" + clientName + "</span>";
        } else {
          h1Elements[i].textContent = "Transformação digital de criação de proposta para novos clientes que vamos entrar em contato.";
        }
      }
    }
    
    // Substituir a introdução
    var introElements = document.querySelectorAll("p");
    for (var j = 0; j < introElements.length; j++) {
      if (introElements[j].textContent.includes("Uma proposta personalizada de automação") || 
          introElements[j].textContent.includes("elevar a experiência dos seus clientes")) {
        console.log("Substituindo a introdução...");
        introElements[j].textContent = "Uma proposta de ter propostas sendo geradas de forma dinamica.";
      }
    }
  }, 500); // Aguardar 500ms para o React renderizar
});
