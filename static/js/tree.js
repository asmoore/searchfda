function makeAdverseEvent(adverseEvent,chartName) {
    visitObj($('#json-viewer'), adverseEvent[0]);
}

function visitObj($container, jsonData) {

    var $ul = $('<ul class="report">');
    
    var $li = $('<li>')
    $li.append('<h5>General Information</h5>');
    $ul.append($li);

    var $li = $('<li>');
    receiveDate = jsonData['receivedate'];
    $li.append('<span class="json-key">Date: </span>');
    $li.append('<span class="date">' + receiveDate + '</span>');
    $ul.append($li);

    var $li = $('<li>');
    occurCountry = jsonData['occurcountry'];
    $li.append('<span class="json-key">Country of occurence: </span>');
    $li.append('<span class="date">' + occurCountry + '</span>');
    $ul.append($li);

    var $li = $('<li>');
    serious = jsonData['serious'];
    if (serious=="1"){
        $li.append('<span class="json-key">Serious: </span>');
        $li.append('<span class="date">' + 'The adverse event resulted in death, a life threatening condition, hospitalization, disability, congenital anomali, or other serious condition.' + '</span>');
        $ul.append($li);
    }
    else {
        $li.append('<span class="json-key">Country of occurence: </span>');
        $li.append('<span class="date">' + 'Not serious' + '</span>');
        $ul.append($li);
    }
    
    
     var $li = $('<li>')
    $li.append('<h5>Reactions</h5>');
    $ul.append($li);
    
    for (var i=0; i<jsonData['patient']['reaction'].length; i++) {
        
        var $li = $('<li>');
        reaction = jsonData['patient']['reaction'][i]['reactionmeddrapt'];
        $li.append('<span class="json-value">' + reaction + '</span>');
        $ul.append($li);
    
    }
    
    var $li = $('<li>')
    $li.append('<h5>Drugs used</h5>');
    $ul.append($li);
    
    for (var i=0; i<jsonData['patient']['drug'].length; i++) {
        
        var $li = $('<li>')
        dosage = jsonData['patient']['drug'][i]['drugdoseagetext'];
        $li.append('<span class="json-key">Dosage: </span>');
        $li.append('<span class="json-value">' + dosage + '</span>')
        $ul.append($li);

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
        $li.append('<span class="break"> </span>')
        $ul.append($li);
                    
    }
    $container.append($ul);
}

