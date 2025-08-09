def gps_consistency(exif_dict):
    # Basit bir örnek kural: Software alanı 'Snapchat' vb ise ve GPSInfo yoksa uyarı
    software = str(exif_dict.get('Software', '')).lower()
    has_gps = 'GPSInfo' in exif_dict
    issues = []
    if 'snapchat' in software and not has_gps:
        issues.append('Software=Snapchat ama GPS bilgisi yok.')
    return {'gps_uyari': issues or None}
