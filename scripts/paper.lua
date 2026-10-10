-- Keep published Markdown portable; apply typesetting-only attributes here.
function Header(element)
  local title = pandoc.utils.stringify(element.content)
  if title == 'Abstract' or title == 'References' then
    element.classes:insert('unnumbered')
  end
  return element
end

function Image(element)
  element.attributes.width = '95%'
  return element
end
