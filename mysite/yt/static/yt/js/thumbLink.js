function thumbLink () {
    var k, j, str, parent;
    var i = document.getElementsByClassName('thumb');
    var len = i.length;
    for(j = 0;j < len; j++)
    {
        k = i[j].getAttribute('src');
        console.log(i);
        str = "https://www.youtube.com/watch?v=" + k.substring(23, 34);
        console.log(str);
        parent = i[j].parentElement;
        parent.setAttribute('href', str);
        parent.setAttribute('target','_blank');
    }
}