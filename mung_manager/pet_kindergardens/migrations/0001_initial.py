# Generated by Django 4.2.11 on 2024-04-07 22:59

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayOff',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='day_off_id', db_comment='휴무 아이디', primary_key=True, serialize=False)),
                ('day_off_at', models.DateField(db_comment='휴무 날짜')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_comment='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, db_comment='수정 일시')),
            ],
            options={
                'db_table': 'day_off',
            },
        ),
        migrations.CreateModel(
            name='KoreaSpecialDay',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='korea_special_day_id', db_comment='한국 공휴일 아이디', primary_key=True, serialize=False)),
                ('name', models.CharField(db_comment='공휴일 이름', max_length=64)),
                ('special_day_at', models.DateField(db_comment='공휴일 날짜')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_comment='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, db_comment='수정 일시')),
            ],
            options={
                'db_table': 'korea_special_day',
            },
        ),
        migrations.CreateModel(
            name='PetKindergarden',
            fields=[
                ('id', models.AutoField(auto_created=True, db_column='pet_kindergarden_id', db_comment='펫 유치원 아이디', primary_key=True, serialize=False)),
                ('name', models.CharField(db_comment='유치원 이름', max_length=64)),
                ('main_thumbnail_url', models.URLField(db_comment='메인 썸네일')),
                ('profile_thumbnail_url', models.URLField(db_comment='프로필 썸네일 이미지')),
                ('phone_number', models.CharField(blank=True, db_comment='전화번호', max_length=16)),
                ('visible_phone_number', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=16), db_comment='노출 전화번호', size=2)),
                ('business_hours', models.CharField(db_comment='영업 시간', max_length=64)),
                ('road_address', models.CharField(db_comment='도로명 주소', max_length=128)),
                ('abbr_address', models.CharField(db_comment='지번 주소', max_length=128)),
                ('detail_address', models.CharField(blank=True, db_comment='상세 주소', max_length=128)),
                ('short_address', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), db_comment='간단 주소', size=10)),
                ('guide_message', models.TextField(blank=True, db_comment='안내 메시지')),
                ('latitude', models.DecimalField(db_comment='위도', decimal_places=6, max_digits=8)),
                ('longitude', models.DecimalField(db_comment='경도', decimal_places=6, max_digits=9)),
                ('point', django.contrib.gis.db.models.fields.PointField(db_comment='위치 좌표', srid=4326)),
                ('reservation_availability_option', models.CharField(choices=[('당일 예약 가능', 'SAME_DAY_AVAILABILITY'), ('당일 예약 불가', 'SAME_DAY_UNAVAILABILITY')], db_comment='예약 가능 설정', max_length=64)),
                ('reservation_change_option', models.CharField(choices=[('당일 변경 가능', 'SAME_DAY_CHANGE'), ('당일 변경 불가', 'SAME_DAY_UNCHANGE')], db_comment='예약 변경 설정', max_length=64)),
                ('daily_pet_limit', models.SmallIntegerField(db_comment='일일 펫 제한')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_comment='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, db_comment='수정 일시')),
            ],
            options={
                'db_table': 'pet_kindergarden',
            },
        ),
        migrations.CreateModel(
            name='RawPetKindergarden',
            fields=[
                ('id', models.AutoField(auto_created=True, db_comment='펫 유치원 로우 아이디', primary_key=True, serialize=False)),
                ('thum_url', models.URLField(db_column='thumUrl', db_comment='썸네일 이미지')),
                ('tel', models.CharField(db_column='tel', db_comment='전화번호', max_length=16)),
                ('virtual_tel', models.CharField(blank=True, db_column='virtualTel', db_comment='가상 전화번호', max_length=16)),
                ('name', models.CharField(db_column='name', db_comment='이름', max_length=64)),
                ('x', models.DecimalField(db_column='x', db_comment='경도', decimal_places=6, max_digits=9)),
                ('y', models.DecimalField(db_column='y', db_comment='위도', decimal_places=6, max_digits=8)),
                ('business_hours', models.CharField(db_column='businessHours', db_comment='영업 시간', max_length=64)),
                ('address', models.CharField(db_column='address', db_comment='주소', max_length=128)),
                ('road_address', models.CharField(db_column='roadAddress', db_comment='도로명 주소', max_length=128)),
                ('abbr_address', models.CharField(db_column='abbrAddress', db_comment='지번 주소', max_length=128)),
                ('short_address', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), db_column='shortAddress', db_comment='간단 주소', size=10)),
            ],
            options={
                'db_table': 'raw_pet_kindergarden',
            },
        ),
    ]