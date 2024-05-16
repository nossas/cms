import pytest

from django import forms

from contrib.ds.blocks.forms import BlockForm, BlockTemplateForm


base_fields = [
    "template",
    "element",
    "layout",
    "is_container",
    "background_image",
    "background_size",
]


def test_fields_block_tempalte_form():
    assert base_fields == BlockTemplateForm.Meta.untangled_fields


def test_fields_block_form():
    assert base_fields == BlockForm.Meta.untangled_fields


def test_template_hidden_on_block_form():
    form = BlockForm()
    assert isinstance(form.fields["template"].widget, forms.HiddenInput)
