default_configurations = (


dict(name='simple.conf', config='''
  mode : "textareas",
  theme : "advanced",
  theme_advanced_toolbar_location : "top",
  theme_advanced_buttons1 : "bold,italic,link,unlink",
  theme_advanced_buttons2 : "",
  theme_advanced_buttons3 : ""
'''
),

dict(name='advanced.conf', config='''
//Sample stuff to get you started,
language : "en",
mode : "textareas",
theme : "advanced",
relative_urls : false,
plugins : "table,save,advhr,iespell,insertdatetime,preview,searchreplace,contextmenu,paste,directionality,fullscreen,noneditable",
theme_advanced_blockformats : "p,div,h3,h4,h5,h6,blockquote,dt,dd,pre,code,samp",
theme_advanced_buttons3 : "",
theme_advanced_buttons2 : "bold,italic,strikethrough,bullist,numlist,separator,undo,redo,separator,link,unlink,image,separator,cleanup,code,removeformat,charmap,fullscreen,copy,paste,pastetext,pasteword",
theme_advanced_buttons1 : "formatselect",
theme_advanced_toolbar_location : "top",
theme_advanced_toolbar_align : "left",
theme_advanced_path_location : "bottom",
plugin_insertdate_dateFormat : "%d-%m-%Y",
plugin_insertdate_timeFormat : "%H:%M:%S",
width: 600,
extended_valid_elements : "hr[class|width|size|noshade],div[id|class],noscript,script,object[id|classid|width|height|codebase|data|type|style],param[name|value],embed[id|type|width|height|src|base|bgcolor|salign|allowFullScreen|menu|style|flashvars],iframe[scrolling|src|width|height|frameborder],table[class],tr[class],td[class],th[class|style],tbody[class],thead[class]",
//external_link_list_url : "example_data/example_link_list.js",
//external_image_list_url : "example_data/example_image_list.js",
//flash_external_list_url : "example_data/example_flash_list.js",
//file_browser_callback : "mcFileManager.filebrowserCallBack",
theme_advanced_resize_horizontal : false,
theme_advanced_resizing : true
'''
),
)
