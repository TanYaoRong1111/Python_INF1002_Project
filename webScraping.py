import requests
import pandas as pd

def webScrapingLazadaSingapore(query, page):

    url = "https://www.lazada.sg/tag/"

    payload = ""
    #Use Headers to pretend to be like a real user and avoid website CAPTCHA
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "bx-v": "2.5.28",
        "cache-control": "no-cache",
        "cookie": "__wpkreporterwid_=b4d7ccff-bb1c-4b8a-b718-07c9b5ccf0c2; hng=SG|en-SG|SGD|702; hng.sig=ryBKXOqZIsp9xOQ3YsZRgD7f-p0UaGB2pZ4BbZM8uEc; lzd_cid=a13f012f-8624-4ad7-9dc8-dbbc84b90fc8; lzd_sid=1a201335f16e59855a6216f64e810458; _tb_token_=eee83e8e1b5a1; lwrid=AgGUsgZZYNFFMoqdDx90X39uIynw; t_fv=1738153548695; t_uid=8cMNlB3v52KYbCgWza1yXHqFHiz3pwk8; t_sid=OIE9thrwkRCa1WSGC2l9BrLM4jyiHwMk; utm_channel=NA; lwrtk=AAEEZ5qOzI1Oc1Y+8DDOnHsu/9A4cQ2peEf+dA6uI7UHbEEQDq/mq4A=; _m_h5_tk=55fc2f722ea8b65c7d9d1fff625e8c16_1738162909736; _m_h5_tk_enc=5781b3a59f951133883c017b4b9074c9; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434a6539364c7747454a7536733550372f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070794d44557759575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441784d4441774d4441774d4441774d4441304e7a6b774e7a6c6a4d6a59334d6d49315957526c4e54646a597a45304d6a55334d4441774d4441774d4441774d5452684f5749335a5445354d3251355a6d4d7959544e695a546b775a546468595749304e6a4a6b5a6d5a6b222c22733b32223a2237383735346666643064306265626534227d; tfstk=gVGnTdt2UvyBDkoAvcPBhUnnW7vOAwN7h0C827EyQlr1vMCKzUVo-0cJR4rdqcqzT8ML2kEuZ4iDWndvM2gQN8-vDIhuLviTNuR8adFwmrOvpndvM2khACHeDXBmprrUz7zUYk7wSzU84_ozU1uafzaPYz5eSVr_bz5zU8Ra7yUcTuozaF0afzPz4vdNFomIDf-MAu9uSy4jsy230V21a_DGMJqq8lfz5faHaouUj_5uv3NX_V0pxsgTOVo0kDdNtm0j1c4Z0QxgNcMr4zmwGgFIHDGbIV9V_VF3X-zq_U542XDtulVczBugtk2q9JAVamuizxei6ERbtWrEeWgRoH3itD3Is4QPQWVKI-c3gIsU2A3mZzcWVCmmlfig7mRkYglhQtroR_awyfW5FJz_SoCsJ5UAsIrT8FYGhCyU5yOMSFX5FJz_SoLMStWaLPaBs; epssw=7*fsdss6Y25sTpCas6ssss6uoLMJDjXDwZkgoZBsjjU_KKzFTCIeb-38O_g21csuojss7vvloZkBDj7BDjssssUwWSvIkhGUzu1usjJKMnissCUANbsssFswbgmF2j1-HEscDcu4mnV4iO78zY8KB5B2D-aCPkUhi-GsAuQU-n6sdYd_F8CDKJE-ONu6sKmBYsCy9bB-fhOmnt6sN2BtMHEiUZiZucOijpMXOr-ijKqYvt-lZRNauu_sIVzxUH_kHl_B6WicXqiAEhR4C9oObssssxWzYhLvCsVMfLLSLlgRrbGueT7UmYasddV9RiCViOsRxrCoLJw63zOA5hpD3UOUOb-We8OK9JtiwGskveN6h.; isg=BMjIpXBcO3GeBFYqF9icg8XImTbacSx7fGCtGoJ5FMM2XWjHKoH8C15b0b0t9uRT",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.lazada.sg/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-csrf-token": "eb01e357e70b5"
     
    }

    res = []

    # For Loop 
    for i in range(int(page)):
        #Fills that can be changed for the web request
        querystring = {
            "ajax": "true",
            "catalog_redirect_tag": "true",
            "page": str(i+1),
            "q": query,
            "spm": "a2o42.homepage.search.d_go"
        }


        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        data = response.json()

        for p in data['mods']['listItems']:
            res.append(p)

    return res

def webScrapingLazadaMalaysia(query, page):

    url = "https://www.lazada.com.my/tag/laptop"


    payload = ""
    headers = {
        "cookie": "__wpkreporterwid_=e1cf4dfd-23ed-4d30-a53c-2af5a8261fd5; lzd_cid=47f445a0-f354-4310-8e13-90696875bc67; lzd_sid=1658cd6bfbba2538749402c075f89e66; _tb_token_=e5ee7b6d0ee83; t_fv=1738050991840; t_uid=pxao2K6OJI4CI7fceK9cq6XpeMXidzHw; __itrace_wid=6ee1c277-c672-4e21-3171-6f3d5c8fb24b; hng=MY|en-MY|MYR|458; userLanguageML=en; lwrid=AgGUq%2Bl3Js5hynCxeV83X39uIynw; lwrtk=AAEEZ5lusP1RTqgAIvf6tC92S8u7M6WgxrvFVM3Fdhdh1pI/Q1snFgU=; _m_h5_tk=4dc1664db9f235f3bb3baa8023fcc064_1738094046166; _m_h5_tk_enc=05ca09a6dc465c23c1fea87fbe25167e; t_sid=c5zH2NqXS75Fbbt5HBSm2yOGcaJld9tB; utm_channel=NA; x5sectag=85984; tfstk=g8uKx_61qdvHiUUD-etgZmE4T-RMo4he5vlfr82hVAHtGjW3VYxeVzHqeug3-XmtyX2NrBu3RQU-ajw3EyTEIAmsbaqHUekiIciad8VnZUeSLyZrx823ezhrHCvDoEcETzrWnKYDPvorOzyWrztg5H6gP69DoEcITzzWnK0hXpjbL7a7Oua5fCFuwzN7PYw_fSNcdzaSFCe_a7bCOJZ51PNUC8a7PYG667kpMQ2148_-DTyTEstana_SWWE6mXw157uT9oejOoQ5PCNLv-GQBKPNPeEsau3PaaeIOmkzGv6BnklSXAFLyFjQlfnSH5uBo9FZxfG0CjCPzX4KDqUIvdSa-v3_52iANaGTJJr71vBpB-gE1qz_jEOx1VknTVhlNUNinRGERzLXgyUQdPFZrd7QeciS-kzPdKqENcHT9rsruq0vxnW0H7jp6CIP4kNZ73r5M2bSV4PTnBKl4grMc5eD6CIP4kNa6-AikgSzjn1..; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434c4f33354c77474550625a6b4a7a2b2f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070794d44557759575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441784d4441774d4441774d4441774d4441304e7a6b774e7a6c6a4d6a59334d6d49315957526c4e54686d4e47517a596d55784d4441774d4441774d4441774d546b784f444a6a4d5449344d6a4d304f5751324d32526d4f5756694e5745314d4442694e574d334d44517a222c22733b32223a2239666638393935396135336438616431227d; epssw=7*6Dhss6pt4ae6-ssussssussKSTbjX4XsE3sOMvcEcap1NP3ecMbXPXQ8r4EcF0ojhVReTbdQsE3Wvhg4ssssssssss3XT9aL6Z61D2laqOb4MNTnvBHybtpsTQzLNNcjOlnQpYDM7n8Ul7EA6zXA8Q9Eh5PpCUT9ePwGAQLgIdy7y0UKvh1B43Xt6xjuuGoJB-QyI6sdiNW5CyNs-tN_uC-bXUOtzD1zUWftuHCOuPOtOTB9BxUmkH6scZ6ZORVEXIpyfPVwmOEyx_4N4xUs2p-XOa6hCoBmeasQ6UsoTJVtrbXbOsus4BDO233VshuoOauIOW2dsh6sBdZtWT2WmduN3RBhqmfpgd9kRS9QTMC-",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "bx-v": "2.5.28",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.lazada.com.my/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-csrf-token": "e5ee7b6d0ee83"
    }

    res = []

    # For Loop 
    for i in range(int(page)):
        #Fills that can be changed for the web request
        querystring = {
            "ajax": "true",
            "catalog_redirect_tag": "true",
            "page": str(i+1),
            "q": query,
            "spm": "a2o42.homepage.search.d_go"
        }


        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        data = response.json()

        for p in data['mods']['listItems']:
            res.append(p)

    return res



def webScrapingLazadaIndonesia(query, page):

    url = "https://www.lazada.co.id/tag/"

 
    payload = ""
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie": "__wpkreporterwid_=74b2a03c-24e4-4a70-9b76-77c4b986d139; lzd_cid=bd398481-5349-433e-8b28-f33f5a0c52c9; lzd_sid=1db808f2dcdcad13744547a13aa94195; _tb_token_=3b6eee7301bf0; t_fv=1738053458312; t_uid=JkCyFMKiesnAwwp8ASRqFSnMVQ32UL5y; hng=ID|id|IDR|360; userLanguageML=id; lwrid=AgGUrA8aGhKrAnYQFTDpX39uIynw; lwrtk=AAEEZ5kH0hEWXwiL/QuzWObGuhg4I875xbvFVM3Fdhdh1pI/Q1snFgU=; t_sid=NqPLVt6G5pmCjvZBRXeBH8kybr1XO5Ci; _m_h5_tk=60102753eb4aab13e385144384653644_1738072641975; _m_h5_tk_enc=a4e836b2dfde1f57b4617442f8c8e03f; x5sec=7b22617365727665722d6c617a6164613b33223a22617c4349582f34727747454d536f3764722f2f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070794d44557759575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441784d4441774d4441774d4441774d4441304e7a6b774e7a6c6a4d6a59334d6d49315957526c4e574e6c4f545a6c4e6a5a6b4d4441774d4441774d4441774d54677759324e694f444d304d7a45304d5755334e474a6c4e6a646c4f546c6b4e546c6b4d6a4269597a4a69222c22733b32223a2266623433343835316230373237353132227d; utm_origin=https://www.google.com/; utm_channel=SEO; tfstk=g-isgQtd31fsIX1nICpUNb35nxqjhjtPltwxExINHlEOMsH8ToJGuF2bcWG0_r3wiXNQjDuN05RgcxhzcQRy43kiIrqvaQosb4mL281OMszT9wE4hteWquMiIoXHTcPXyAfXSihxMohYvWeuFoBTBSpQJ-y7DGUAXwCLt-EYD-Expke4eNCxMopIpW2YDSH32_yX35M6CXIVVcOgXAFCDinTjrF5MWe3LDw_57KuOiHsARa_wAiZWM43pDoQzyW2rkHo8feQVH7T2vgxN4hDzwqsHVh0RfAhRWuKjxFY8tIodYMtykn2HT4I9-a8Dy6ADvZgOjeL23CQK2HZkcc1hieib0zbZy9AmrrK4z3-1tvoplexizm2ZGVtHYmozutFWuHIkbgf4sjzN3IAl9alcJNydp_cof-wkiXushBTWJ2_Ap9C1kUTKJNydp_coPe3Lw9Bd1Zd.; epssw=7*rnyss6EJdsF1CBDjT28vvasKs0B8zQXss6dOMtKI70VNvUswF6qLPeIOg21csssdssdjNguehs3vT28v7BDjggsvBqNEsw317C08nFbsnvw49EssmlmWdDglBZFNP9iBTAwrNhcK8065hXmDY7jHPvm5C0Y1JoAiw7WDa6puVafaGO2sCDxOHWQOOXEdsxjSVEMJEPQKOXSXLspsmkYOgXjKKqAt-spsusxlBRb-lD9Jgla1ln3R9oSAYSpUAeY5Dt7jmNA68VTVgs6hufeOsGwXCQlCXqXeCD0Jgs6xsd_h3kf8ZsIkrv2tvT2UEsBh-i2DsKahP6Zas_HKMHb.",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.lazada.co.id/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-csrf-token": "3b6eee7301bf0"
    }

    res = []

    # For Loop 
    for i in range(int(page)):
        #Fills that can be changed for the web request
        querystring = {
            "ajax": "true",
            "catalog_redirect_tag": "true",
            "page": str(i+1),
            "q": query,
            "spm": "a2o42.homepage.search.d_go"
        }


        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        data = response.json()

        for p in data['mods']['listItems']:
            res.append(p)

    return res
    

def webScrapingLazadaThailand(query, page):

    url = "https://www.lazada.co.th/tag/laptop"

    payload = ""
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "bx-v": "2.5.28",
        "cache-control": "no-cache",
        "cookie": "lzd_cid=d72d445d-5e2f-4acd-88f8-5c116d1ec1b6; lzd_sid=13a1925ef7d144e639f8a701f2ddbc75; _tb_token_=e06db668b3bee; t_fv=1738057895713; t_uid=LzdiXwKkubtEzAHjZwdeVCLoLVfsftCt; t_sid=NrGKSz5WUNSQEU8w7m3H7Z1hggJyUAnA; utm_origin=https://www.google.com/; utm_channel=SEO; hng=TH|en|THB|764; userLanguageML=en; lwrid=AgGUrFLPaSQFi5%2BUvQA6X39uIynw; _m_h5_tk=6168e1dbcb3a4518aca585178071f555_1738066896315; _m_h5_tk_enc=d81d96e781f47d2f62b6a6d748c9df05; lwrtk=AAEEZ5kZKMxOfJVyuobnDP17DLhmKW3zEbvFVM3Fdhdh1pI/Q1snFgU=; tfstk=gV6i2Eazg1RsDc7-WwJ_Ny-XeoNdfc9f3ZHvkKL4Te8IWVHO0ovcjZXYfiz1o6j57FkY1OQnnwbWHGLOH9cVyiHOXdIAKZbk-xQY11EDnwby7Pw_CwQdVwbDGlTvuEbA01ELe8I1fK92oze8eUbHhvXMuqp2CpWGSTrge8I1bK94yzeRBmnuDF823CRaLX8BmhJ2_nrH8nxSgV723kqH0hoZ_C8Z8H-9jK8VuKrhYetqpnGXrN_RLyql27W1JZXHjCYPxWMqn6MJsU79-xoNKh0wzG8n3x8Too2FxGUiFMp1YaxRWJkGrg6C-H7znyvfRs72mwySkd1R5TOhA7kFvdYpa3WU0Y8AI6Iy-Lm4QMvMSQW9s8kVzMjVwBXL489MQF5vCinuWMXGWG6hDmleIdCHZOvzFV8A9gXDmtabKaj5dwxFz-4N49lEaEjshHrAKjGX_HtHyvs9p3nmzkWUxkc7LC-BfJq3xjGX_HtHykqnaXRwAhwh.; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434b375234727747454b54492f7254392f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070794d44557759575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441784d4441774d4441774d4441774d4441304e7a6b774e7a6c6a4d6a59334d6d49315957526c4e54686b4e5751785a444d7a4d4441774d4441774d4441774d54466d4f4449794e7a4d344e5467344e6a49315a4745334e3249304f57566d4d6a4177596a517a5a546469222c22733b32223a2234643730386262323332613461333835227d; epssw=7*7W1ss6E2ssLYYsssssssus36STO_jDwZvwlgon5MAUBLyBVZWE3bIiQ8r4EcsG8W7BDsuuDjT28vTahuef58AwlavzJoTo_bsd2J4j3v7j81veVdhaPznFtlEzg79arQq5KSdwWWN3LX8Kn_Y3xZA_Lg289qVbG6scsEPZ1duxju-kDdsRQyI6ItClFdOFIt8PcStt0HBjSivRadsuNlOiXt-OQtgyBy7bjkCDaZ3h_ECSMUl2O773byK0D2mjmUicdBua0JgksgsEdhCpsoijV7vassORrbsaZLOW2dsdahn6ZEs3Bhmd3kSi9tN60Y3zBh4dSTEQHs",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.lazada.co.th/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-csrf-token": "e06db668b3bee"
    }

    res = []

    # For Loop 
    for i in range(int(page)):
        #Fills that can be changed for the web request
        querystring = {
            "ajax": "true",
            "catalog_redirect_tag": "true",
            "page": str(i+1),
            "q": query,
            "spm": "a2o42.homepage.search.d_go"
        }


        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        data = response.json()

        for p in data['mods']['listItems']:
            res.append(p)

    return res

def webScrapingLazadaPhilippines(query, page):

    url = "https://www.lazada.com.ph/tag/laptop"

    payload = ""
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie": "lzd_cid=96265a25-c6e5-4dcd-af48-3015267ffac6; t_fv=1738058114779; t_uid=PDKK05UsjHrBb6nZDo3PiMKNoCZbL4ia; hng=PH|en-PH|PHP|608; lwrid=AgGUrFYnK8nSGGjUwNo%2FX39uIynw; lzd_sid=13b2522187a1c61e1beba06a5cef85b9; _tb_token_=71f37fe3716ee; t_sid=fz9o1ETxradD7mReQw40b6FP9L0lUxCT; utm_origin=https://www.google.com/; utm_channel=SEO; _m_h5_tk=e85fa0f6d752bed831e7eb8eff95e302_1738949752074; _m_h5_tk_enc=b8b30124cc01fb3d938f05d0e413bb7c; lwrtk=AAEEZ6aTN4PkH62jBSkd1T4pLV5lDltO503OyqGYxfSazrgSka0MGOo=; tfstk=gUKsvyiL35V6FlPHIfHFN02tF3jjaIizW-6vEKEaHGITMSpRTikguVXfc6Oc_NJA0-OBEION6i-2GEOyn1hijcAeTLAB0fmijBRF9KUNuF5ahRxBNorZsVvYciSxabor4dvNmihPirF6E1XDpsHFWeZ41dsxaboUh8hq2idwyqwLOpChhtCAHIIdv6XVHiCOkWUde6CADIEA9pBGUsFAkiHBp6XADsdADvF3atMV1dM1MzVXd0XJB6ZYDhnG5_97uoEvDO_1RdCChttCCN1R-YO__hdeHh-G-bNRmp8WGEdmzyj6HFIOUdm_Agp98n6e0xzf6CxBphbQEujXWCTAreiurNQf1eKOR-EvKMTBMEOs1Pf97B_lpwejq9RP9dx9RxVpBQ51X9QE2Y9dke-GrhlLfgLkQG8vi4zhfKLOAgPa4_i8DrwCroBCavMQorAZbqEmVJY1hNBhCMMId5sdW9XCavMQorbOK9zIdvN1v; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434e2b6a6d4c3047454d75766e61622b2f2f2f2f2f77456943584a6c5932467764474e6f59544333774d756b413070794d44557759575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441784d4441774d4441774d4441774d4441304e7a6b774e7a6c6a4d6a59334d6d49315957526c4e5759304e4455325a444a694d4441774d4441774d4441774d5449304e6a686c4e44566a4e446334596a41334d4751334e4455784e7a5a6b4e6a4d314d5445774e545577222c22733b32223a2264393734643865333463666436383735227d; isg=BMLCqf7WETuLoA1ZlcjHRFbsE8gkk8atCiIXNAzavjXgX2bZ9CaovcncC1MjUj5F; epssw=7*BTzss6YfrEr5cG81ssssuuoLMJo8zQXsvwaOMX2AGbig7VQmw5pzIZFjg21F7w8W7pDjNE72M1dssuDj7BmvTfDj9GlF3WHpGNoWO2NTwLksninrCeDjmlojf_Et5FRD3W_yFGWTCWaoLEDEIoWQoyXkNnBIYRgwuwE2zWRj7kFLVeV5APjuusBb2PjKOXgIOWQHfbiQ-XVdrW1hvEJBs-2UJBugOW9iQspACypsnUDuOlU4N-eMOZfbbSuJxliAHKTqmOF7V9ej3hQhwpDxORahZJqxCvaAgcGFuSXT5ijhORJ4cOuk-YoXgd0dua0fg63dCmLJciUG3KVsmd3Y3K0JJ60YCWFhUxqSTPyV",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.lazada.com.ph/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-csrf-token": "eb33b3307e36e"
    }

    res = []

    # For Loop 
    for i in range(int(page)):
        #Fills that can be changed for the web request
        querystring = {
            "ajax": "true",
            "catalog_redirect_tag": "true",
            "page": str(i+1),
            "q": query,
            "spm": "a2o42.homepage.search.d_go"
        }


        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        data = response.json()

        for p in data['mods']['listItems']:
            res.append(p)

    return res

