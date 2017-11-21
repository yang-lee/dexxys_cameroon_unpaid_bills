# -*- coding: ascii -*-
from openerp import models, fields, api
from datetime import date
import StringIO
import base64

class Invoice(models.Model):
    _inherit = 'account.account.template'


    def send_unpaid_vendor_bills_via_email(self, cr, uid, context=None):

        """ Cette fonction permet d'envoyer des notifications sur les factures client non regles. """

        header_label_list=["Caissier(e)", "Client", "Reference", "Montant", "Reste", "Date Paie.", "Date Fact."]
        template_obj = self.pool.get('mail.template')
        template_ids = template_obj.search(cr, uid, [('name', '=', 'Dexxys Cameroon Vendor Bills Alert Template')])
        template = template_obj.browse(cr, uid, template_ids)
        journal_object = self.pool.get('account.journal')
        journal_ids = journal_object.search(cr, uid, [('type', '=', 'sale')])
        invoice_obj  = self.pool.get('account.invoice')
        partner_obj = self.pool.get('res.partner')
        saleperson_obj = self.pool.get('res.users')
        default_body = template.body_html
        for journal in journal_object.browse(cr, uid, journal_ids):
            seller = ""
            if template:

                header_body = """
                        <div style="">
                            <h3 style="color:#000;font-weight:600;text-transform:uppercase">%s <span style="font-weight:600; margin-left:2px">[ %s ] </span></h3>

                        </div>
                """ %(journal.name, journal.code)
                custom_body  = """
                    <table class="table-border" style"border:1px solid #ccc;text-transform:uppercase">
                        <th style="padding-left:25px; text-align:left;text-transform:uppercase">%s</th>
                        <th style="padding-left:25px; text-align:left;text-transform:uppercase">%s</th>
                        <th style="padding-left:25px; text-align:left;text-transform:uppercase">%s</th>
                        <th style="padding-left:25px; text-align:left;text-transform:uppercase">%s</th>
                        <th style="padding-left:25px; text-align:left;text-transform:uppercase">%s</th>
                        <th style="padding-left:25px; text-align:left;text-transform:uppercase">%s</th>
                        <th style="padding-left:25px; text-align:left;text-transform:uppercase">%s</th>
                """ %(header_label_list[0], header_label_list[1], header_label_list[2], header_label_list[3], header_label_list[4], header_label_list[5], header_label_list[6])

                invoice_ids  = invoice_obj.search(cr, uid, [('residual', '>', 0), ('journal_id', '=', journal.id)])
                total = 0

                #   On parcourt la liste des factures non regles et on recupere les invoice_ids

                for invoice in invoice_obj.browse(cr, uid, invoice_ids):
                    _id = invoice.partner_id
                    _user = invoice.user_id
                    partner_inv = ""
                    saleperson_inv = ""
                    if _id:
                        partner = partner_obj.browse(cr, uid,  _id.id, context=context)
                        partner_inv = partner.display_name


                    if _user:
                        saleperson = saleperson_obj.browse(cr, uid, _user.id, context=context)
                        saleperson_inv = saleperson.display_name

                    if invoice.payment_term_id:
                        payment = self.pool.get('account.payment.term').browse(cr, invoice.payment_term_id.id, context=context)

                        date_inv = payment.name
                    name_inv = invoice.display_name


                    total_inv = invoice.amount_total
                    residual_inv = invoice.residual
                    date_inv = invoice.date_due
                    date_create = invoice.date_invoice
                    total += int(residual_inv)
                    custom_body += """
                        <tr style="font-size:13px; border-bottom:1px solid #ccc">
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                            <td style="padding-left:25px; text-align:left">%s</td>
                        </tr>
                    """ %(saleperson_inv, partner_inv, name_inv, '{0:,}'.format(int(total_inv)), '{0:,}'.format(int(residual_inv)), date_inv, date_create)

                footer_body = """
                        <div style="float:right;margin-bottom:20px">
                            <div style="">
                                <h5 style="font-weight:600">TOTAL RESTE<span style="font-weight:600; color:#2196F3;margin-left:20px">%s </span></h5>
                            </div>
                        </div>
                        <div style="height:1px ; background:#ccc; margin: 45px 0;"></div>
                """ %('{0:,}'.format(int(total)))
                custom_body  += "</table>"
            template.body_html += header_body  + custom_body + footer_body
        send_email = template_obj.send_mail(cr, uid, template.id, uid, force_send=True, context=context)
        template.body_html = default_body
        return True
