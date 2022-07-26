function itemDesc(kingTags, context)
{
    var a, b, c, i, j, item;
    for (i = 0; i < kingTags.length; i++)
    {
        try
        {
            item = document.getElementById(kingTags[i]);
            a = document.createElement('SPAN');
            a.setAttribute('class', 'itemCount');
            a.innerText = context[kingTags[i]]['count'] + " Channels";
            item.appendChild(a);
            c = document.createElement("DIV");
            c.setAttribute('class', 'itemDesc');
            item.appendChild(c);
            b = document.createElement("DIV");
            b.setAttribute('class', 'imageBox');
            b.innerHTML = '';
            for (j = 0; j < context[kingTags[i]]['images'].length; j++)
            {
                b.innerHTML += '<img src=' + context[kingTags[i]]['images'][j] + ' class="itemImage">';
            }
            c.appendChild(b);
        }
        catch(e)
        {
            continue;
        }
    }
}