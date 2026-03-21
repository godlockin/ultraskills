# 常见敏感数据模式

用于 BFG `--replace-text` 的 banned.txt 文件模板。

## AWS 凭证

```text
# AWS Access Key ID (示例，替换为实际密钥)
AKIAIOSFODNN7EXAMPLE

# AWS Secret Access Key (示例)
wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# 使用正则匹配所有 AWS Access Key
regex:AKIA[0-9A-Z]{16}
```

## GitHub Token

```text
# Personal Access Token 格式
regex:ghp_[0-9a-zA-Z]{36}
regex:gho_[0-9a-zA-Z]{36}
regex:ghu_[0-9a-zA-Z]{36}
regex:ghs_[0-9a-zA-Z]{36}
regex:ghr_[0-9a-zA-Z]{36}
```

## 私钥

```text
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN OPENSSH PRIVATE KEY-----
-----BEGIN DSA PRIVATE KEY-----
-----BEGIN EC PRIVATE KEY-----
-----BEGIN PGP PRIVATE KEY BLOCK-----
```

## 数据库连接字符串

```text
# MySQL
mysql://root:password@

# PostgreSQL
postgres://user:password@

# MongoDB
mongodb://user:password@
```

## API 密钥通用模式

```text
# 常见 API Key 格式
regex:api[_-]?key[=:]\s*[0-9a-zA-Z]{32,}
regex:Authorization:\s*Bearer\s+[0-9a-zA-Z]{20,}
```

## 文件密码

```text
# 常见密码模式（根据实际情况修改）
password123
admin123
secret
changeme
```

## 使用方式

1. 复制需要的模式到 `banned.txt`
2. 修改示例值为实际需要替换的敏感数据
3. 运行 BFG：

```bash
bfg --replace-text banned.txt repo.git
```

## 注意事项

- 每行一个敏感字符串
- 使用 `regex:` 前缀进行正则匹配
- 使用 `glob:` 前缀进行通配符匹配
- 不加前缀则为精确匹配
