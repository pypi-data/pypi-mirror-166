from .context import DATADIR
from model.common.commonmodel import CommonModel, BuilderModel
from model.bcpnp.data import JobOffer
from model.common.person import Person
from model.common.wordmaker import WordMaker
import os
from pydantic import BaseModel


class Personal(Person):
    def __str__(self):
        return self.full_name


class JobDescriptionModel(BaseModel, BuilderModel):
    personal: Personal
    joboffer: JobOffer

    def context(self, *args, **kwargs):
        context = {**self.dict(), "requirements": self.joboffer.requirements}
        return context

    def make_pdf_form(self, *args, **kwargs):
        pass

    def make_web_form(self, *args, **kwargs):
        pass


class JobDescriptionModelE(CommonModel, JobDescriptionModel):
    def __init__(self, excels=None, output_excel_file=None):
        mother_excels = ["excel/er.xlsx", "excel/pa.xlsx"]
        super().__init__(excels, output_excel_file, mother_excels, globals())
