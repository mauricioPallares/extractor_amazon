function main(splash, args)

    splash:on_request(
        function(request)

            request:set_proxy{
                host = "{ip}",
                port = {port},
                username = "{proxy_user}",
                password = "{proxy_pass}",
                type = "SOCKS5"
            }
        end
    )
    splash:go(args.url)

    splash:wait(0.5)

    return splash:html()

end