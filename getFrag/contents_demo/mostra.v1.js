  function mostra(toContext) {
    var idX = $('#busca1').val().trim();
    var id, id_lc, id_sub;
    id = id_lc = idX.toLowerCase();
    var item_pos = id_lc.indexOf('item');
    if (item_pos!==-1) {
      id = id_lc.substr(0,item_pos);
      id_sub = idX.substr(item_pos+4);
      //alert("tem item em "+item_pos+'... novo id='+id+"\nsub="+id_sub);
    }
    var obj = document.getElementById(id);
    if (obj) {
      var htm = obj.innerHTML;
      if (id_sub){  // pode usar jQuery .next() mas é gambi pois pode ter um paragrafo no meio.
        alert("Não implementado seletor de items aqui, use a API XML.\nNo formato desta página só pega em XPath tratando-a como XHTML, nao HTML5");
        //$subObj = $(obj).find('li');
        // if $subObj.length
        // var msg = $subObj[id_sub-1].html();
        // if (!msg) msg = "?? item "+id_sub+" não encontrado!";
        // htm = htm+"<br/>...<br/>"+msg;
      }
      $('#mostraqui').html( htm );
      if (id && toContext!=undefined) {  //confirm("Posicionar a tela no contexto?")){
        var h = '#'+id;        
        window.location.hash = h;
        $('html, body').animate({ scrollTop: $(h).offset().top }, 'slow');
      }
    }
    else
      alert("ID ''"+id+"''\n não encontrado.")
  }

  window.onload = function() {
    // Prepare the URL
    var hash_id = window.location.hash.trim();
    if (hash_id) {
      hash_id = hash_id.substr(1);
      $('#busca1').val(hash_id);
  	  mostra();
    }
  }
