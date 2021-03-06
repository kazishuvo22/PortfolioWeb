from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
# image compression method
from tinymce.models import HTMLField


def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=50)
    new_image = File(im_io, name=image.name)
    return new_image


class General(models.Model):
    name = models.CharField(max_length=300, verbose_name="Enter your name")
    advertise_title = models.CharField(max_length=300, verbose_name="Advertisement Title")
    terms = HTMLField(verbose_name="Enter terms and conditions", null=True, blank=True)
    hero_image_field = models.FileField(verbose_name="Home Background hero image", upload_to='Homepage_images',
                                        help_text="Only PNG, JPG, JPEG format supported",
                                        validators=[FileExtensionValidator(
                                            allowed_extensions=['png', 'jpg', 'jpeg'])])
    last_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    policy = HTMLField(verbose_name="Enter policy", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Company official Mobile/ Phone number")
    email = models.EmailField(verbose_name="Enter Personal Email")
    address = models.CharField(max_length=300, verbose_name="Full Address ")
    facebook_link = models.CharField(max_length=300, verbose_name="Facebook Link ",
                                     help_text="Add 'http:// or https://' before your web address if not inserted, "
                                               "Example:(http://example.com)")
    whatsapp_link = models.CharField(max_length=300, verbose_name="Whatsapp Link/Mobile number")
    instagram_link = models.CharField(max_length=300, verbose_name="Instagram Link",
                                      help_text="Add 'http:// or https://' before your web address if not inserted, "
                                                "Example:(http://example.com)")
    linkedin_link = models.CharField(max_length=300, verbose_name="Linkedin Link",
                                     help_text="Add 'http:// or https://' before your web address if not inserted, "
                                               "Example:(http://example.com)")
    youtube_link = models.CharField(max_length=300, verbose_name="Youtube Link",
                                    help_text="Add 'http:// or https://' before your web address if not inserted, "
                                              "Example:(http://example.com)")

    mode = models.CharField(max_length=100, verbose_name="Select Mode",
                            choices=(('1', 'production'), ('2', 'development')))
    last_edited = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        if ('request') in kwargs and self.last_author is None:
            request = kwargs.pop('request')
            self.last_author = request.user
        new_image = compress(self.hero_image_field)
        self.hero_image_field = new_image
        super(General, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class About(models.Model):
    general = models.ForeignKey(General, on_delete=models.DO_NOTHING)
    short_about = models.TextField(max_length=300, verbose_name="Site Short About",
                                   help_text="Not more than 300 character")
    years_of_experience = models.IntegerField(verbose_name="Enter the company work of experiences", blank=True,
                                              null=True)
    about_body_image = models.FileField(verbose_name="About section body image", upload_to='About_image',
                                        help_text="Only PNG, JPG, JPEG format supported",
                                        validators=[FileExtensionValidator(
                                            allowed_extensions=['png', 'jpg', 'jpeg'])])
    last_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    long_about = HTMLField(verbose_name="Site Long About", null=True, blank=True)
    last_edited = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        if ('request') in kwargs and self.last_author is None:
            request = kwargs.pop('request')
            self.last_author = request.user
        new_image = compress(self.about_body_image)
        self.about_body_image = new_image
        super(About, self).save(*args, **kwargs)

    def __str__(self):
        return self.short_about


class Contact(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=256)
    message = models.TextField()
    ctime = models.DateTimeField()


class Project(models.Model):
    name = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    Detail = HTMLField(verbose_name="Project Details", null=True, blank=True)
    project_image = models.FileField(verbose_name="Project Image", upload_to='project_image',
                                     help_text="Only PNG, JPG, JPEG format supported",
                                     validators=[FileExtensionValidator(
                                         allowed_extensions=['png', 'jpg', 'jpeg'])])
    start_date = models.DateField(verbose_name="Project Start Date", blank=True, null=True)
    end_date = models.DateField(verbose_name="Project End Date", blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkExperience(models.Model):
    position = models.CharField(max_length=300, verbose_name="Enter Designation/Position")
    company_name = models.CharField(max_length=300, verbose_name="Company or Organization Name")
    responsibilities = HTMLField(verbose_name="Company/Organization Responsibilities")
    start_date = models.DateField(verbose_name="Join Date", blank=True, null=True)
    end_date = models.DateField(verbose_name="End Date", blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name + "-" + self.position


class Education(models.Model):
    institute_name = models.CharField(max_length=300, verbose_name="Enter Institute Name")
    degree_full = models.CharField(max_length=300, verbose_name="Enter Your Degree")
    summery = HTMLField(verbose_name="Share Education Summery")
    start_date = models.DateField(verbose_name="Join Date", blank=True, null=True)
    end_date = models.DateField(verbose_name="End Date", blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.institute_name


class References(models.Model):
    person_name = models.CharField(max_length=300, verbose_name="Reference Person Name")
    person_designation = models.CharField(max_length=300, verbose_name="Person Designation")
    person_image = models.FileField(verbose_name="Reference Person Image", upload_to='ref_person_image',
                                    help_text="Only PNG, JPG, JPEG format supported",
                                    validators=[FileExtensionValidator(
                                        allowed_extensions=['png', 'jpg', 'jpeg'])])
    company_name = models.CharField(max_length=300, verbose_name="Company or Organization Name")
    person_email = models.EmailField(verbose_name="Reference Person's Email", blank=True, null=True)
    person_phone = models.CharField(max_length=300, verbose_name="Reference Person's Phone/Mobile Number", blank=True,
                                    null=True)
    quotes = HTMLField(verbose_name="Reference Person's testimonials", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.person_name


skills_type = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Professional', 'Professional'),
    ('Advance', 'Advance'),
    ('Expert', 'Expert'),

)

bootstrap_bg_type = (
    ('bg-primary', 'bg-primary'),
    ('bg-secondary', 'bg-secondary'),
    ('bg-success', 'bg-success'),
    ('bg-danger', 'bg-danger'),
    ('bg-warning', 'bg-warning'),
    ('bg-info', 'bg-info'),
    ('bg-light', 'bg-light'),
    ('bg-dark', 'bg-dark'),
    ('bg-white', 'bg-white'),
)


class Skills(models.Model):
    skills_category_name = models.CharField(max_length=300, verbose_name="Enter Skills Category",
                                            help_text="ex. Framework, Database, etc..")
    title = models.CharField(max_length=300, verbose_name="Skills Title")
    level = models.CharField(max_length=100, choices=skills_type, verbose_name="Skills Level")
    level_value = models.IntegerField(verbose_name="Skills Level Value")
    bootstrap_bg = models.CharField(max_length=100, choices=bootstrap_bg_type, verbose_name="Select Background Color")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


