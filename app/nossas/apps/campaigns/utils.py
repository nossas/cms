import urllib
from django.core.files import File as DjangoFile
from filer.models import Image
from contrib.bonde.models import Mobilization, MobilizationStatus
from .models import Campaign, CampaignStatus, CampaignGroup


def create_filer_image(user, filename, datafile):
    owner = user
    file_obj = DjangoFile(open(datafile, "rb"), name=filename)
    image = Image.objects.create(owner=owner, original_filename=filename, file=file_obj)
    return image


def import_mobilization(mobilization_id, current_site, current_user):
    mobilization = Mobilization.objects.get(id=mobilization_id)

    updated = False
    campaign_group, created = CampaignGroup.on_site.get_or_create(
        name=mobilization.community.name,
        community_id=mobilization.community.id,
        site=current_site
    )

    campaign = Campaign.on_site.create(
        name=mobilization.name,
        description_pt_br=mobilization.goal,
        mobilization_id=mobilization.id,
        hide=True,
        status=CampaignStatus.closed
        if mobilization.status != MobilizationStatus.active
        else CampaignStatus.opened,
        campaign_group=campaign_group,
        site=current_site,
    )

    if mobilization.custom_domain:
        updated = True
        campaign.url = "https://" + mobilization.custom_domain

    if mobilization.theme:
        updated = True
        campaign.tags.add(mobilization.theme.label)

    if mobilization.subthemes.exists():
        updated = True
        campaign.tags.add(
            *list(map(lambda x: x.label, mobilization.subthemes.all()))
        )

    if mobilization.facebook_share_image:
        updated = True
        result = urllib.request.urlretrieve(
            mobilization.facebook_share_image
        )

        image = create_filer_image(
            current_user, f"mobilization_{mobilization.id}_image", result[0]
        )

        campaign.picture = image

    if mobilization.created_at:
        updated = True
        campaign.release_date = mobilization.created_at

    if updated:
        campaign.save()

    return campaign