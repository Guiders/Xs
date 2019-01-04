from django.db import models

# Create your models here.
from XServer.settings import ImageStorage


class Action(models.Model):
    aid = models.IntegerField(primary_key=True, verbose_name='动作id', help_text="动作id")
    videoRes = models.CharField(default='', max_length=200, verbose_name="视频链接", help_text="视频链接")
    actionName = models.CharField(default='', max_length=100, verbose_name="动作名称", help_text="动作名称")
    doItRight = models.TextField(default='', verbose_name="doItRight", help_text="doItRight")
    breathing = models.TextField(default='', verbose_name="breathing", help_text="breathing")
    videoSize = models.IntegerField(default=0, verbose_name="视频大小", help_text="视频大小")
    imgCover = models.CharField(default='', max_length=200, verbose_name="封面图",
                                help_text="封面图")
    duration = models.IntegerField(default=30, verbose_name="单次时长", help_text="单次时长")
    repeatCount = models.IntegerField(default=1, verbose_name="重复次数", help_text="重复次数")
    imgLocal = models.CharField(default='', max_length=200, verbose_name="本地地址", help_text="本地地址")

    class Meta:
        verbose_name = '动作'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_action"

    def __str__(self):
        return self.actionName


class Challenge(models.Model):
    Level = ((1, "1"),
             (2, "2"),
             (3, "3"),
             (4, "4"),
             (5, "5")
             )
    CHARGE_TYPE = (
        (0, "免费"),
        (1, "播放课程观看视频"),
        (2, "进入课程收费")
    )
    challengeId = models.IntegerField(primary_key=True, unique=True, verbose_name="课程id", help_text="课程id")
    challengeName = models.CharField(max_length=100, verbose_name="课程名称", help_text="课程名称")
    imgCover = models.CharField(default='', max_length=200, verbose_name="封面图", help_text="封面图")
    level = models.IntegerField(choices=Level, verbose_name="课程等级", help_text="课程等级")
    pgmIds = models.CharField(max_length=150, verbose_name="课程ids", help_text="课程ids")
    chargeType = models.IntegerField(default=0,choices=CHARGE_TYPE, verbose_name="付费类型",
                                     help_text="付费类型")

    slotid = models.IntegerField(default=0, verbose_name="广告id",
                                     help_text="广告id")


    class Meta:
        verbose_name = '挑战课程'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_challenge"

    def __str__(self):
        return self.challengeName


class Program(models.Model):
    CHARGE_TYPE = (
        (0, "免费"),
        (1, "播放课程观看视频"),
        (2, "进入课程收费")
    )
    PGM_TYPE = (
        (0, "普通课程"),
        (1, "挑战课程"),

    )
    Level = ((1, "1"),
             (2, "2"),
             (3, "3"),
             (4, "4"),
             (5, "5")
             )

    slotid = models.IntegerField(default=0, verbose_name="广告id",
                                 help_text="广告id")
    pgmId = models.IntegerField(primary_key=True, verbose_name='课程id', help_text="课程id")
    programName = models.CharField(default='', max_length=100, verbose_name="课程名称", help_text="课程名称")
    chargeType = models.IntegerField(default=0,choices=CHARGE_TYPE, verbose_name="付费类型",
                                     help_text="付费类型")
    totalTime = models.IntegerField(default=0, verbose_name="总时长", help_text="总时长")
    kcal = models.IntegerField(default=0, verbose_name="卡路里", help_text="卡路里")
    level = models.IntegerField(choices=Level, verbose_name="等级", help_text="等级")
    programDesc = models.TextField(default="", blank=True, null=True, verbose_name="课程描述", help_text="课程描述")
    pgmType = models.IntegerField(choices=PGM_TYPE, verbose_name="课程类型", help_text="课程类型")
    imgCover = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="封面图", help_text="封面图")
    imgCoverBig = models.CharField(default='', blank=True, null=True, max_length=200, verbose_name="封面大图",
                                   help_text="封面大图")
    restIndexArray = models.CharField(default='', blank=True, null=True, max_length=100, verbose_name="休息Index",
                                      help_text="休息Index")
    actionIds = models.CharField(default='', max_length=100, verbose_name="课程ids", help_text="课程ids")
    challenge = models.ForeignKey(Challenge, null=True, blank=True, on_delete=models.CASCADE, verbose_name="所属挑战课程",
                                  help_text="所属挑战课程", to_field='challengeId')

    class Meta:
        verbose_name = '课程'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_program"

    def __str__(self):
        if self.challenge is None:
            return self.programName
        else:
            return self.programName + "_" + self.challenge.challengeName


class LanguageBase(models.Model):
    language = models.CharField(max_length=20, verbose_name="语言", help_text="语言")
    version= models.BigIntegerField(default=0,verbose_name="版本", help_text="版本")

    class Meta:
        verbose_name = '多语言及json'
        # 复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.language


class LanguageAction(models.Model):
    language = models.ForeignKey(LanguageBase, on_delete=models.CASCADE, verbose_name="语言", help_text="语言")
    action = models.ForeignKey(Action, on_delete=models.CASCADE, verbose_name="所属动作",
                               help_text="所属动作", to_field='aid')

    actionName = models.CharField(default='', max_length=100, verbose_name="动作名称", help_text="动作名称")
    doItRight = models.TextField(default='', verbose_name="doItRight", help_text="doItRight")
    breathing = models.TextField(default='', verbose_name="breathing", help_text="breathing")

    class Meta:
        verbose_name = '动作多语言'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_language_action"
        unique_together = ('language', 'action',)


    def __str__(self):
        return self.actionName


class LanguageProgram(models.Model):
    language = models.ForeignKey(LanguageBase, on_delete=models.CASCADE, verbose_name="语言", help_text="语言")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="所属课程", help_text="所属课程",
                                to_field="pgmId")

    programName = models.CharField(default='', max_length=100, verbose_name="课程名称", help_text="课程名称")
    programDesc = models.TextField(default="", verbose_name="课程描述", help_text="课程描述")

    class Meta:
        verbose_name = '课程多语言'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_language_program"
        unique_together = ('language', 'program',)


    def __str__(self):
        return self.programName


class LanguageChallenge(models.Model):
    language = models.ForeignKey(LanguageBase, on_delete=models.CASCADE, verbose_name="语言", help_text="语言")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, verbose_name="所属挑战课程", help_text="所属挑战课程",
                                  to_field="challengeId")
    challengeName = models.CharField(max_length=100, verbose_name="课程名称", help_text="课程名称")

    class Meta:
        verbose_name = '挑战课程多语言'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_language_challenge"
        unique_together = ('language', 'challenge',)

    def __str__(self):
        return self.challengeName


class Image(models.Model):
    IMG_TYPE = ((1, "普通封面图"),
                (2, "视频封面"),
                )

    def get_photo_path(instance, filename):
        dir_name = ''
        if instance.imgType == 1:
            dir_name = 'imgs'
        elif instance.imgType == 2:
            dir_name = 'video_cover'

        return '{dir_name}/{filename}'.format(dir_name=dir_name, filename=filename)

    imgType = models.IntegerField(default=1, choices=IMG_TYPE, verbose_name="图片类型", help_text="图片类型")
    img = models.ImageField(upload_to=get_photo_path, storage=ImageStorage(), verbose_name="图片", help_text="图片")

    class Meta:
        verbose_name = '图片'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_image"

    def __str__(self):
        return self.img.path


class ChallengeSort(models.Model):
    position = models.IntegerField(default=0, verbose_name="排序字段", help_text="排序字段")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, verbose_name="所属挑战课程", help_text="所属挑战课程",
                                  to_field="challengeId")

    class Meta:
        verbose_name = '挑战课程排序'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_challenge_sort"

    def __str__(self):
        return self.challenge.challengeName


class ProgramSort(models.Model):
    position = models.IntegerField(default=0, verbose_name="排序字段", help_text="排序字段")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="所属课程", help_text="所属课程",
                                to_field="pgmId")

    class Meta:
        verbose_name = '普通课程排序'
        # 复数
        verbose_name_plural = verbose_name
        db_table = "sport_program_sort"

    def __str__(self):
        return self.program.programName

# class ChallengeProgram(models.Model):
#     challenge = models.ForeignKey(Challenge, null=True, blank=True, on_delete=models.CASCADE)
#     program = models.ForeignKey(Program, null=True, blank=True, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = '课程关系'
#         # 复数
#         verbose_name_plural = verbose_name
#         db_table = 'sport_challenge_program'
#         unique_together = ('challenge', 'program')
#
#     def __str__(self):
#         return self.challenge.challengeName
