# SmartDNS 列表

```
# 兜底 DNS
server-https https://223.5.5.5/dns-query
server-https https://doh.pub/dns-query

# 国内常见域名使用运营商 DNS
server 202.96.128.86 -group domestic -exclude-default-group
server 202.96.128.166 -group domestic -exclude-default-group

# 推荐使用 fakeip 模式
server 127.0.0.1:1053 -group proxy -exclude-default-group


# 屏蔽广告，配置文件或域名集合，二选一
conf-file /etc/smartdns/conf.d/adblock-domains.conf
#domain-set -name adblock -file /etc/smartdns/domain-set/adblock-domains.txt
#address /domain-set:adblock/#

domain-set -name domestic -file /etc/smartdns/domain-set/china-domains.txt
domain-rules /domain-set:domestic/ -nameserver domestic

domain-set -name proxy -file /etc/smartdns/domain-set/proxy.txt
domain-rules /domain-set:proxy/ -nameserver proxy -speed-check-mode none -no-cache
```
