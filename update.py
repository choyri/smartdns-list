#!/usr/bin/env python3

import urllib.request


def parse_clash_format(content):
    """
    解析 Clash 格式的文件
    只处理 DOMAIN-SUFFIX 和 DOMAIN 行
    返回域名列表，每个元素是 (domain, is_suffix) 元组
    """
    domains = []

    for line in content.split('\n'):
        line = line.strip()

        # 跳过空行和注释
        if not line or line.startswith('#'):
            continue

        # 处理 DOMAIN-SUFFIX
        if line.startswith('DOMAIN-SUFFIX,'):
            domain = line.replace('DOMAIN-SUFFIX,', '', 1)
            domains.append((domain, True))  # True 表示是 suffix

        # 处理 DOMAIN
        elif line.startswith('DOMAIN,'):
            domain = line.replace('DOMAIN,', '', 1)
            domains.append((domain, False))  # False 表示是完整域名

    return domains


def parse_dnsmasq_format(content):
    """
    解析 dnsmasq 格式的文件
    格式：server=/example.com/1.1.1.1
    返回域名列表，每个元素是 (domain, is_suffix) 元组
    """
    domains = []

    for line in content.split('\n'):
        line = line.strip()

        # 跳过空行和注释
        if not line or line.startswith('#'):
            continue

        # 处理 server= 格式
        if line.startswith('server=/'):
            # 提取域名部分：server=/example.com/1.1.1.1
            parts = line.split('/')
            if len(parts) >= 3:
                domain = parts[1]
                domains.append((domain, True))  # dnsmasq 格式默认是 suffix

    return domains


def parse_plain_format(content, is_suffix):
    """
    解析纯域名格式的文件
    每行一个域名
    """
    domains = []

    for line in content.split('\n'):
        line = line.strip()
        if line:
            domains.append((line, is_suffix))

    return domains


def save_txt(all_domains, filename):
    """
    保存纯域名 txt 文件
    """
    domains_txt = [domain for domain, _ in all_domains]

    # 去重并排序
    domains_txt = sorted(set(domains_txt))

    # 保存 txt 文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(domains_txt))

    print(f"已生成: {filename} (共 {len(domains_txt)} 个域名)")


def save_adblock_domains(all_domains):
    """
    保存 adblock 域名到 txt 和 conf 文件
    转换规则：
    - suffix 域名 -> address /example.com/#
    - 完整域名 -> address /-.example.com/#
    """
    domains_txt = []
    domains_conf = []

    for domain, is_suffix in all_domains:
        domains_txt.append(domain)
        if is_suffix:
            domains_conf.append(f"address /{domain}/#")
        else:
            domains_conf.append(f"address /-.{domain}/#")

    # 去重并排序
    domains_txt = sorted(set(domains_txt))
    domains_conf = sorted(set(domains_conf))

    # 保存 txt 文件
    with open('adblock-domains.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(domains_txt))

    # 保存 conf 文件
    with open('adblock-domains.conf', 'w', encoding='utf-8') as f:
        f.write('\n'.join(domains_conf))

    print(f"已生成: adblock-domains.txt (共 {len(domains_txt)} 个域名)")
    print(f"已生成: adblock-domains.conf (共 {len(domains_conf)} 条规则)")


def update_china_domains():
    """
    更新中国域名列表
    只生成 txt
    """
    print("=" * 50)
    print("开始更新 China Domain 列表")
    print("=" * 50)

    all_domains = []

    # 处理 ChinaDomain.list (Clash 格式)
    url1 = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/ChinaDomain.list"
    try:
        print(f"正在下载: {url1}")
        with urllib.request.urlopen(url1) as response:
            content = response.read().decode('utf-8')
        domains = parse_clash_format(content)
        all_domains.extend(domains)
        print(f"  解析完成: {len(domains)} 个域名")
    except Exception as e:
        print(f"  错误: {e}")

    # 处理 apple.china.conf (dnsmasq 格式)
    url2 = "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/refs/heads/master/apple.china.conf"
    try:
        print(f"正在下载: {url2}")
        with urllib.request.urlopen(url2) as response:
            content = response.read().decode('utf-8')
        domains = parse_dnsmasq_format(content)
        all_domains.extend(domains)
        print(f"  解析完成: {len(domains)} 个域名")
    except Exception as e:
        print(f"  错误: {e}")

    # 处理 google.china.conf (dnsmasq 格式)
    url3 = "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/refs/heads/master/google.china.conf"
    try:
        print(f"正在下载: {url3}")
        with urllib.request.urlopen(url3) as response:
            content = response.read().decode('utf-8')
        domains = parse_dnsmasq_format(content)
        all_domains.extend(domains)
        print(f"  解析完成: {len(domains)} 个域名")
    except Exception as e:
        print(f"  错误: {e}")

    # 保存域名
    if all_domains:
        print(f"\n总计: {len(all_domains)} 个域名")
        save_txt(all_domains, 'china-domains.txt')
    else:
        print("\n没有解析到任何域名")


def update_adblock_domains():
    """
    更新广告拦截域名列表
    生成 txt 和 conf
    """
    print("\n" + "=" * 50)
    print("开始更新 AdBlock Domain 列表")
    print("=" * 50)

    all_domains = []

    # 处理 BanAD.list (Clash 格式)
    url1 = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/refs/heads/master/Clash/BanAD.list"
    try:
        print(f"正在下载: {url1}")
        with urllib.request.urlopen(url1) as response:
            content = response.read().decode('utf-8')
        domains = parse_clash_format(content)
        all_domains.extend(domains)
        print(f"  解析完成: {len(domains)} 个域名")
    except Exception as e:
        print(f"  错误: {e}")

    # 处理 domain.txt (纯完整域名格式)
    url2 = "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/refs/heads/build/rule/domain.txt"
    try:
        print(f"正在下载: {url2}")
        with urllib.request.urlopen(url2) as response:
            content = response.read().decode('utf-8')
        domains = parse_plain_format(content, is_suffix=False)
        all_domains.extend(domains)
        print(f"  解析完成: {len(domains)} 个域名")
    except Exception as e:
        print(f"  错误: {e}")

    # 处理 domain_suffix.txt (纯 suffix 域名格式)
    url3 = "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/refs/heads/build/rule/domain_suffix.txt"
    try:
        print(f"正在下载: {url3}")
        with urllib.request.urlopen(url3) as response:
            content = response.read().decode('utf-8')
        domains = parse_plain_format(content, is_suffix=True)
        all_domains.extend(domains)
        print(f"  解析完成: {len(domains)} 个域名")
    except Exception as e:
        print(f"  错误: {e}")

    # 保存域名
    if all_domains:
        print(f"\n总计: {len(all_domains)} 个域名")
        save_adblock_domains(all_domains)
    else:
        print("\n没有解析到任何域名")


if __name__ == '__main__':
    update_china_domains()
    update_adblock_domains()
    print("\n" + "=" * 50)
    print("全部更新完成!")
    print("=" * 50)


