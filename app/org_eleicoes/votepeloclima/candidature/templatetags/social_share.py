from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def share_url(base_url, slug, platform):
    url = f"{base_url}/c/{slug}"

    if platform == 'whatsapp':
        text = ("Oi! As eleições estão chegando e o futuro da nossa cidade depende do nosso voto. "
                "Compartilho com você uma das candidaturas comprometidas na luta pelo meio ambiente e contra as ameaças climáticas. "
                "Conheça as propostas na plataforma *Vote pelo Clima!*")
        return f"https://wa.me/?text={urlencode({'text': text})}{url}"

    elif platform == 'twitter':
        text = ("O clima mudou. A política precisa mudar. #VotePeloClima é a plataforma que reúne candidaturas de todo o Brasil "
                "comprometidas com a pauta climática, eu sou uma delas! Acesse o perfil e conheça as propostas.")
        return f"https://twitter.com/intent/tweet?url={url}&{urlencode({'text': text})}"

    elif platform == 'linkedin':
        title = "O clima mudou. A política precisa mudar."
        summary = ("#VotePeloClima é a plataforma que reúne candidaturas de todo o Brasil comprometidas com a pauta climática, "
                   "eu sou uma delas! Acesse o perfil e conheça as propostas.")
        return f"https://www.linkedin.com/shareArticle?mini=true&url={url}&{urlencode({'title': title, 'summary': summary})}"

    elif platform == 'facebook':
        quote = ("O clima mudou. A política precisa mudar. #VotePeloClima é a plataforma que reúne candidaturas de todo o Brasil "
                 "comprometidas com a pauta climática, eu sou uma delas! Acesse o perfil e conheça as propostas.")
        return f"https://www.facebook.com/sharer/sharer.php?u={url}&{urlencode({'quote': quote})}"

    return url