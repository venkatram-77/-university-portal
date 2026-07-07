$certThumbprint = "1DDDCD2CD1B9101F69D7C864643DCBA113DE3631"
$cert = Get-Item -LiteralPath "Cert:\CurrentUser\My\$certThumbprint"

# Export cert as PEM
$certData = $cert.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)
$pemCert = "-----BEGIN CERTIFICATE-----`n" + [System.Convert]::ToBase64String($certData, [System.Base64FormattingOptions]::InsertLineBreaks) + "`n-----END CERTIFICATE-----"
Set-Content -Path "cert.pem" -Value $pemCert

# Export private key as PEM
$rsa = [System.Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)
$keyBytes = $rsa.ExportPkcs8PrivateKey()
$pemKey = "-----BEGIN PRIVATE KEY-----`n" + [System.Convert]::ToBase64String($keyBytes, [System.Base64FormattingOptions]::InsertLineBreaks) + "`n-----END PRIVATE KEY-----"
Set-Content -Path "key.pem" -Value $pemKey

Write-Output "Cert and key exported"
Test-Path "cert.pem"
Test-Path "key.pem"
