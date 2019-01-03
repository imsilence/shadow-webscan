#encoding: utf-8

FEATURES = [
    ('lnmp', 'regex', {'path' : '/p.php', 'regex' : r'<title>PHP探针\s*for\s*LNMP一键安装包</title>'}),
    ('thinkphp', 'md5', {'path' : '/', 'md5' : ''}),
    ('nginx', 'headers', {'path' : '/', 'headers' : ('server', 'nginx')}),
    ('httpd', 'headers', {'path' : '/', 'headers' : ('server', 'httpd')}),
    ('lighttpd', 'headers', {'path' : '/', 'headers' : ('server', 'lighttpd')}),
    ('php', 'headers', {'path' : '/', 'headers' : ('set-cookie', 'phpsession')}),
    ('php', 'headers', {'path' : '/', 'headers' : ('x-powered-by', 'php')}),
]