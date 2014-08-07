function makeAdverseEvent(adverseEvent,chartName) {
    visitObj($('#json-viewer'), adverseEvent[0]);
}

function visitObj($container, jsonData) {
    var $ul = $('<ul class="report">');
    
    var $li = $('<li>');
    receiveDate = jsonData['receivedate'];
    $li.append('<span class="json-key">Date: </span>');
    $li.append('<span class="date">' + receiveDate + '</span>');
    $ul.append($li);
    
     var $li = $('<li>')
    $li.append('<h2>Reactions</h2>');
    $ul.append($li);
    
    for (var i=0; i<jsonData['patient']['reaction'].length; i++) {
        
        var $li = $('<li>');
        reaction = jsonData['patient']['reaction'][i]['reactionmeddrapt'];
        $li.append('<span class="json-value">' + reaction + '</span>');
        $ul.append($li);
    
    }
    
    var $li = $('<li>')
    $li.append('<h2>Drugs used</h2>');
    $ul.append($li);
    
    for (var i=0; i<jsonData['patient']['drug'].length; i++) {
        
        var $li = $('<li>')
        indication = jsonData['patient']['drug'][i]['drugindication'];
        $li.append('<span class="json-key">Indication: </span>');
        $li.append('<span class="json-value">' + indication + '</span>')
        $ul.append($li);
    
        var $li = $('<li>')
        medicinalProduct = jsonData['patient']['drug'][i]['medicinalproduct'];
        $li.append('<span class="json-key">Medicinal Product: </span>');
        $li.append('<span class="json-value">' + medicinalProduct + '</span>')
        $ul.append($li);
    
        var $li = $('<li>')
        drugManufacturer = jsonData['patient']['drug'][i]['openfda']['manufacturer_name'][0];
        $li.append('<span class="json-key">Drug manufacturer: </span>');
        $li.append('<span class="json-value">' + drugManufacturer + '</span>')
        $ul.append($li);
    
        var $li = $('<li>')
        route = jsonData['patient']['drug'][i]['openfda']['route'];
        $li.append('<span class="json-key">Route: </span>');
        $li.append('<span class="json-value">' + route + '</span>')
        $ul.append($li);
                
        var $li = $('<li>')
        $li.append('<span class="break"> </span>')
        $ul.append($li);
                
    }

   
    $container.append($ul);
}

