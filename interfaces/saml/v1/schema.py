# Copyright 2023 Canonical
# See LICENSE file for licensing details.
"""This file defines the schema for the provider side of the saml interface.

It exposes one interfaces.schema_base.DataBagSchema subclass called:
- ProviderSchema

Examples:
    ProviderSchema:
        unit: <empty>
        app: {"saml":
                 {
                    "metadata_url": "https://login.ubuntu.com/saml/metadata",
                    "metadata": "
                        <md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" entityID="https://login.ubuntu.com">
                            <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
                            <md:KeyDescriptor use="signing">
                                <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                                    <ds:X509Data>
                                        <ds:X509Certificate>MIICjzCCAfigAwIBAgIJALNN/vxaR1hyMA0GCSqGSIb3DQEBBQUAMDoxCzAJBgNVBAYTAkdCMRMwEQYDVQQIEwpTb21lLVN0YXRlMRYwFAYDVQQKEw1DYW5vbmljYWwgTHRkMB4XDTEyMDgxMDEyNDE0OFoXDTEzMDgxMDEyNDE0OFowOjELMAkGA1UEBhMCR0IxEzARBgNVBAgTClNvbWUtU3RhdGUxFjAUBgNVBAoTDUNhbm9uaWNhbCBMdGQwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMM4pmIxkv419q8zj5EojK57y6plU/+k3apX6w1PgAYeI0zhNuud/tiqKVQEDyZ6W7HNeGtWSh5rewy8c07BShcHG5Y8ibzBdIibGs5k6gvtmsRiXDE/F39+RrPSW18beHhEuoVJM9RANp3MYMOK11SiClSiGo+NfBKFuoqNX3UjAgMBAAGjgZwwgZkwHQYDVR0OBBYEFH/no88pbywRnW6Fz+B4lQ04w/86MGoGA1UdIwRjMGGAFH/no88pbywRnW6Fz+B4lQ04w/86oT6kPDA6MQswCQYDVQQGEwJHQjETMBEGA1UECBMKU29tZS1TdGF0ZTEWMBQGA1UEChMNQ2Fub25pY2FsIEx0ZIIJALNN/vxaR1hyMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEArTGbZ1rg++aBxnNuJ7eho62JKKtRW5O+kMBvBLWi7fKck5uXDE6d7Jv6hUy/gwUZV7r5kuPwRlw3Pu6AX4R60UsQuVG1/VVVI7nu32iCkXx5Vzq446IkVRdk/QOda1dRyq0oaifUUhJfwVFSsm95ENDFdGqD0raj7g77ajcBMf8=</ds:X509Certificate>
                                    </ds:X509Data>
                                </ds:KeyInfo>
                            </md:KeyDescriptor>
                            <md:KeyDescriptor use="encryption">
                                <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                                    <ds:X509Data>
                                        <ds:X509Certificate>MIICjzCCAfigAwIBAgIJALNN/vxaR1hyMA0GCSqGSIb3DQEBBQUAMDoxCzAJBgNVBAYTAkdCMRMwEQYDVQQIEwpTb21lLVN0YXRlMRYwFAYDVQQKEw1DYW5vbmljYWwgTHRkMB4XDTEyMDgxMDEyNDE0OFoXDTEzMDgxMDEyNDE0OFowOjELMAkGA1UEBhMCR0IxEzARBgNVBAgTClNvbWUtU3RhdGUxFjAUBgNVBAoTDUNhbm9uaWNhbCBMdGQwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMM4pmIxkv419q8zj5EojK57y6plU/+k3apX6w1PgAYeI0zhNuud/tiqKVQEDyZ6W7HNeGtWSh5rewy8c07BShcHG5Y8ibzBdIibGs5k6gvtmsRiXDE/F39+RrPSW18beHhEuoVJM9RANp3MYMOK11SiClSiGo+NfBKFuoqNX3UjAgMBAAGjgZwwgZkwHQYDVR0OBBYEFH/no88pbywRnW6Fz+B4lQ04w/86MGoGA1UdIwRjMGGAFH/no88pbywRnW6Fz+B4lQ04w/86oT6kPDA6MQswCQYDVQQGEwJHQjETMBEGA1UECBMKU29tZS1TdGF0ZTEWMBQGA1UEChMNQ2Fub25pY2FsIEx0ZIIJALNN/vxaR1hyMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEArTGbZ1rg++aBxnNuJ7eho62JKKtRW5O+kMBvBLWi7fKck5uXDE6d7Jv6hUy/gwUZV7r5kuPwRlw3Pu6AX4R60UsQuVG1/VVVI7nu32iCkXx5Vzq446IkVRdk/QOda1dRyq0oaifUUhJfwVFSsm95ENDFdGqD0raj7g77ajcBMf8=</ds:X509Certificate>
                                    </ds:X509Data>
                                </ds:KeyInfo>
                            </md:KeyDescriptor>
                            <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://login.ubuntu.com/+logout"/>
                            <md:NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:email</md:NameIDFormat>
                            <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://login.ubuntu.com/saml/"/>
                            </md:IDPSSODescriptor>
                        </md:EntityDescriptor>
                    ",
                    "entity_id": "https://login.ubuntu.com",
                    "single_sign_on_service_redirect_url": "https://login.ubuntu.com/saml/",
                    "single_sign_on_service_redirect_binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
                    "single_logout_service_redirect_url": "https://login.ubuntu.com/+logout",
                    "single_logout_service_redirect_binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect",
                    "x509certs": "-----BEGIN CERTIFICATE-----\n
                        MIIC6DCCAdCgAwIBAgIUW42TU9LSjEZLMCclWrvSwAsgRtcwDQYJKoZIhvcNAQEL\n
                        BQAwIDELMAkGA1UEBhMCVVMxETAPBgNVBAMMCHdoYXRldmVyMB4XDTIzMDMyNDE4\n
                        NDMxOVoXDTI0MDMyMzE4NDMxOVowPDELMAkGA1UEAwwCb2sxLTArBgNVBC0MJGUw\n
                        NjVmMWI3LTE2OWEtNDE5YS1iNmQyLTc3OWJkOGM4NzIwNjCCASIwDQYJKoZIhvcN\n
                        AQEBBQADggEPADCCAQoCggEBAK42ixoklDH5K5i1NxXo/AFACDa956pE5RA57wlC\n
                        BfgUYaIDRmv7TUVJh6zoMZSD6wjSZl3QgP7UTTZeHbvs3QE9HUwEkH1Lo3a8vD3z\n
                        eqsE2vSnOkpWWnPbfxiQyrTm77/LAWBt7lRLRLdfL6WcucD3wsGqm58sWXM3HG0f\n
                        SN7PHCZUFqU6MpkHw8DiKmht5hBgWG+Vq3Zw8MNaqpwb/NgST3yYdcZwb58G2FTS\n
                        ZvDSdUfRmD/mY7TpciYV8EFylXNNFkth8oGNLunR9adgZ+9IunfRKj1a7S5GSwXU\n
                        AZDaojw+8k5i3ikztsWH11wAVCiLj/3euIqq95z8xGycnKcCAwEAATANBgkqhkiG\n
                        9w0BAQsFAAOCAQEAWMvcaozgBrZ/MAxzTJmp5gZyLxmMNV6iT9dcqbwzDtDtBvA/\n
                        46ux6ytAQ+A7Bd3AubvozwCr1Id6g66ae0blWYRRZmF8fDdX/SBjIUkv7u9A3NVQ\n
                        XN9gsEvK9pdpfN4ZiflfGSLdhM1STHycLmhG6H5s7HklbukMRhQi+ejbSzm/wiw1\n
                        ipcxuKhSUIVNkTLusN5b+HE2gwF1fn0K0z5jWABy08huLgbaEKXJEx5/FKLZGJga\n
                        fpIzAdf25kMTu3gggseaAmzyX3AtT1i8A8nqYfe8fnnVMkvud89kq5jErv/hlMC9\n
                        49g5yWQR2jilYYM3j9BHDuB+Rs+YS5BCep1JnQ==\n
                        -----END CERTIFICATE-----\n"
                }
             }
"""
from interface_tester.schema_base import DataBagSchema
from pydantic import AnyHttpUrl, BaseModel, Field
from typing import Optional


class SamlProviderData(BaseModel):
    metadata: str = Field(
        description="IdP's metadata.",
        title="Metadata",
        examples=["""<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" entityID="https://login.ubuntu.com">
            <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
            <md:KeyDescriptor use="signing">
                <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                    <ds:X509Data>
                        <ds:X509Certificate>MIICjzCCAfigAwIBAgIJALNN/vxaR1hyMA0GCSqGSIb3DQEBBQUAMDoxCzAJBgNVBAYTAkdCMRMwEQYDVQQIEwpTb21lLVN0YXRlMRYwFAYDVQQKEw1DYW5vbmljYWwgTHRkMB4XDTEyMDgxMDEyNDE0OFoXDTEzMDgxMDEyNDE0OFowOjELMAkGA1UEBhMCR0IxEzARBgNVBAgTClNvbWUtU3RhdGUxFjAUBgNVBAoTDUNhbm9uaWNhbCBMdGQwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMM4pmIxkv419q8zj5EojK57y6plU/+k3apX6w1PgAYeI0zhNuud/tiqKVQEDyZ6W7HNeGtWSh5rewy8c07BShcHG5Y8ibzBdIibGs5k6gvtmsRiXDE/F39+RrPSW18beHhEuoVJM9RANp3MYMOK11SiClSiGo+NfBKFuoqNX3UjAgMBAAGjgZwwgZkwHQYDVR0OBBYEFH/no88pbywRnW6Fz+B4lQ04w/86MGoGA1UdIwRjMGGAFH/no88pbywRnW6Fz+B4lQ04w/86oT6kPDA6MQswCQYDVQQGEwJHQjETMBEGA1UECBMKU29tZS1TdGF0ZTEWMBQGA1UEChMNQ2Fub25pY2FsIEx0ZIIJALNN/vxaR1hyMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEArTGbZ1rg++aBxnNuJ7eho62JKKtRW5O+kMBvBLWi7fKck5uXDE6d7Jv6hUy/gwUZV7r5kuPwRlw3Pu6AX4R60UsQuVG1/VVVI7nu32iCkXx5Vzq446IkVRdk/QOda1dRyq0oaifUUhJfwVFSsm95ENDFdGqD0raj7g77ajcBMf8=</ds:X509Certificate>
                    </ds:X509Data>
                </ds:KeyInfo>
            </md:KeyDescriptor>
            <md:KeyDescriptor use="encryption">
                <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                    <ds:X509Data>
                        <ds:X509Certificate>MIICjzCCAfigAwIBAgIJALNN/vxaR1hyMA0GCSqGSIb3DQEBBQUAMDoxCzAJBgNVBAYTAkdCMRMwEQYDVQQIEwpTb21lLVN0YXRlMRYwFAYDVQQKEw1DYW5vbmljYWwgTHRkMB4XDTEyMDgxMDEyNDE0OFoXDTEzMDgxMDEyNDE0OFowOjELMAkGA1UEBhMCR0IxEzARBgNVBAgTClNvbWUtU3RhdGUxFjAUBgNVBAoTDUNhbm9uaWNhbCBMdGQwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMM4pmIxkv419q8zj5EojK57y6plU/+k3apX6w1PgAYeI0zhNuud/tiqKVQEDyZ6W7HNeGtWSh5rewy8c07BShcHG5Y8ibzBdIibGs5k6gvtmsRiXDE/F39+RrPSW18beHhEuoVJM9RANp3MYMOK11SiClSiGo+NfBKFuoqNX3UjAgMBAAGjgZwwgZkwHQYDVR0OBBYEFH/no88pbywRnW6Fz+B4lQ04w/86MGoGA1UdIwRjMGGAFH/no88pbywRnW6Fz+B4lQ04w/86oT6kPDA6MQswCQYDVQQGEwJHQjETMBEGA1UECBMKU29tZS1TdGF0ZTEWMBQGA1UEChMNQ2Fub25pY2FsIEx0ZIIJALNN/vxaR1hyMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEArTGbZ1rg++aBxnNuJ7eho62JKKtRW5O+kMBvBLWi7fKck5uXDE6d7Jv6hUy/gwUZV7r5kuPwRlw3Pu6AX4R60UsQuVG1/VVVI7nu32iCkXx5Vzq446IkVRdk/QOda1dRyq0oaifUUhJfwVFSsm95ENDFdGqD0raj7g77ajcBMf8=</ds:X509Certificate>
                    </ds:X509Data>
                </ds:KeyInfo>
            </md:KeyDescriptor>
            <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://login.ubuntu.com/+logout"/>
            <md:NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:email</md:NameIDFormat>
            <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://login.ubuntu.com/saml/"/>
            </md:IDPSSODescriptor>
        </md:EntityDescriptor>"""],
    )
    metadata_url: Optional[AnyHttpUrl] = Field(
        description="URL to the IdP's metadata.",
        title="Metadata URL",
        examples=["https://login.ubuntu.com/saml/metadata"],
    )
    entity_id: AnyHttpUrl = Field(
        description="Identifier of the IdP entity.",
        title="Entity ID",
        examples=["https://login.ubuntu.com"],
    )
    single_sign_on_service_redirect_url: AnyHttpUrl = Field(
        description="URL target of the IdP where the Authentication REDIRECT Request Message will be sent.",
        title="SSO REDIRECT URL",
        examples=["https://login.ubuntu.com/saml/"],
    )
    single_sign_on_service_redirect_binding: str = Field(
        description="SAML protocol binding to be used when returning the REDIRECT <Response> message.",
        title="SSO REDIRECT binding",
        examples=["urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"],
    )
    single_sign_on_service_post_url: Optional[AnyHttpUrl] = Field(
        description="URL target of the IdP where the Authentication POST Request Message will be sent.",
        title="SSO POST response URL",
        examples=["https://login.ubuntu.com/saml/"],
    )
    single_sign_on_service_post_binding: Optional[str] = Field(
        description="SAML protocol binding to be used when returning the POST <Response> message.",
        title="SSO POST binding",
        examples=["urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Post"],
    )
    single_logout_service_url: Optional[AnyHttpUrl] = Field(
        description="URL Location where the <LogoutRequest> from the IdP will be sent (IdP-initiated logout).",
        title="SP Logout URL",
        examples=["https://example.com/logout"],
    )
    single_logout_service_redirect_response_url: Optional[AnyHttpUrl] = Field(
        description="URL Location where the REDIRECT <LogoutResponse> from the IdP will sent (SP-initiated logout, reply): only specify if different from url parameter.",
        title="SSO logout REDIRECT response URL",
        examples=["https://example.com/logout"],
    )
    single_logout_service_redirect_binding: Optional[str] = Field(
        description="SAML protocol binding to be used when returning the REDIRECT <Response> message.",
        title="SSO logout REDIRECT binding",
        examples=["urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"],
    )
    single_logout_service_post_response_url: Optional[AnyHttpUrl] = Field(
        description="URL Location where the POST <LogoutResponse> from the IdP will sent (SP-initiated logout, reply): only specify if different from url parameter.",
        title="SSO logout POST response URL",
        examples=["https://example.com/logout"],
    )
    single_logout_service_post_binding: Optional[str] = Field(
        description="SAML protocol binding to be used when returning the POST <Response> message.",
        title="SSO logout POST binding",
        examples=["urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Post"],
    )
    x509certs: str = Field(
        description="Comma separated list of public X.509 certificates of the IdP.",
        title="Public IdP certificates",
        examples=["""-----BEGIN CERTIFICATE-----
            MIIC6DCCAdCgAwIBAgIUW42TU9LSjEZLMCclWrvSwAsgRtcwDQYJKoZIhvcNAQEL
            BQAwIDELMAkGA1UEBhMCVVMxETAPBgNVBAMMCHdoYXRldmVyMB4XDTIzMDMyNDE4
            NDMxOVoXDTI0MDMyMzE4NDMxOVowPDELMAkGA1UEAwwCb2sxLTArBgNVBC0MJGUw
            NjVmMWI3LTE2OWEtNDE5YS1iNmQyLTc3OWJkOGM4NzIwNjCCASIwDQYJKoZIhvcN
            AQEBBQADggEPADCCAQoCggEBAK42ixoklDH5K5i1NxXo/AFACDa956pE5RA57wlC
            BfgUYaIDRmv7TUVJh6zoMZSD6wjSZl3QgP7UTTZeHbvs3QE9HUwEkH1Lo3a8vD3z
            eqsE2vSnOkpWWnPbfxiQyrTm77/LAWBt7lRLRLdfL6WcucD3wsGqm58sWXM3HG0f
            SN7PHCZUFqU6MpkHw8DiKmht5hBgWG+Vq3Zw8MNaqpwb/NgST3yYdcZwb58G2FTS
            ZvDSdUfRmD/mY7TpciYV8EFylXNNFkth8oGNLunR9adgZ+9IunfRKj1a7S5GSwXU
            AZDaojw+8k5i3ikztsWH11wAVCiLj/3euIqq95z8xGycnKcCAwEAATANBgkqhkiG
            9w0BAQsFAAOCAQEAWMvcaozgBrZ/MAxzTJmp5gZyLxmMNV6iT9dcqbwzDtDtBvA/
            46ux6ytAQ+A7Bd3AubvozwCr1Id6g66ae0blWYRRZmF8fDdX/SBjIUkv7u9A3NVQ
            XN9gsEvK9pdpfN4ZiflfGSLdhM1STHycLmhG6H5s7HklbukMRhQi+ejbSzm/wiw1
            ipcxuKhSUIVNkTLusN5b+HE2gwF1fn0K0z5jWABy08huLgbaEKXJEx5/FKLZGJga
            fpIzAdf25kMTu3gggseaAmzyX3AtT1i8A8nqYfe8fnnVMkvud89kq5jErv/hlMC9
            49g5yWQR2jilYYM3j9BHDuB+Rs+YS5BCep1JnQ==
            -----END CERTIFICATE-----"""],
    )


class ProviderSchema(DataBagSchema):
    """Provider schema for SAML."""
    app: SamlProviderData

class RequirerSchema(DataBagSchema):
    """Requirer schema for SAML."""
