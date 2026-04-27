function gerar_troca(){
    let troca ={
        pessoa_1:document.getElementById('pessoa1').value,
        dia_1:document.getElementById('dia1').value,
        turno_1:document.getElementById('turno1').value,
        pessoa_2:document.getElementById('pessoa2').value,
        dia_2:document.getElementById('dia2').value,
        turno_2:document.getElementById('turno2').value
    }
    for (let chave in troca){
        if (!troca[chave]){
            return;
        }
    }
    return troca;
};


let form = document.querySelector('form');

form.addEventListener('submit',function(event){
    event.preventDefault();
    let botao = document.getElementById('botao')
    botao.disabled = true;
    botao.style.backgroundColor = 'grey'
    let troca = gerar_troca()

    
    if (!troca){
        alert("Dados inválidos!")
        botao.disabled = false;
        botao.style.backgroundColor = '#333'
        return
    }else{
        console.log(troca);

        fetch('http://127.0.0.1:5000/troca',{
            method:'POST',
            headers:{"Content-Type": "application/json"},
            body:JSON.stringify(troca)
        
        }).then(function(resposta){
            if (!resposta.ok){
                throw new Error('ERRO');
            }else{        
                return resposta.json();
            }    
        
        }).then(function(dados){
            console.log(dados)

            alert(`Troca Realizada\n ${dados.pessoa_1}(${dados.dia_1}-${dados.turno_1})\n ${dados.pessoa_2}(${dados.dia_2}-${dados.turno_2})`)
            form.reset()
            botao.disabled = false
            botao.style.backgroundColor = '#333'
        
        }).catch(function(erro){
            alert('erro de envio')
            botao.disabled = false
            botao.style.backgroundColor = '#333'
        })
    }});
