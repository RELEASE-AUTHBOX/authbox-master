from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Content
class Command(BaseCommand):
	help='Migrate hero slideshow to parent-child structure'
	def handle(A,*K,**L):
		E='slideshow-image-01';F='slideshow-image-02';G='slideshow-image-03'
		try:
			with transaction.atomic():
				B=Content.objects.filter(code=E).first();C=Content.objects.filter(code=F).first();D=Content.objects.filter(code=G).first()
				if not B:A.stdout.write(A.style.ERROR(f"Slide 1 not found with code: {E}"));return
				if not C:A.stdout.write(A.style.WARNING(f"Slide 2 not found with code: {F}"))
				if not D:A.stdout.write(A.style.WARNING(f"Slide 3 not found with code: {G}"))
				if C and C.parent_id==B.id:A.stdout.write(A.style.WARNING('Migration already completed - Slide 2 is already a child of Slide 1'));return
				if B.parent_id:A.stdout.write(A.style.NOTICE(f"Removing parent from Slide 1"));B.parent=None;B.save()
				B.order=0;B.save();A.stdout.write(A.style.SUCCESS(f"✓ Slide 1 set as parent (order=0)"))
				if C:C.parent=B;C.order=1;C.save();A.stdout.write(A.style.SUCCESS(f"✓ Slide 2 set as child of Slide 1 (order=1)"))
				if D:D.parent=B;D.order=2;D.save();A.stdout.write(A.style.SUCCESS(f"✓ Slide 3 set as child of Slide 1 (order=2)"))
				A.stdout.write(A.style.NOTICE('\nVerifying migration:'));H=B.get_children();A.stdout.write(A.style.NOTICE(f"Parent: {B.code} (order={B.order})"));A.stdout.write(A.style.NOTICE(f"Children count: {H.count()}"))
				for I in H:A.stdout.write(A.style.NOTICE(f"  - {I.code} (order={I.order})"))
				A.stdout.write(A.style.SUCCESS('\n✅ Migration completed successfully!'))
		except Exception as J:A.stdout.write(A.style.ERROR(f"❌ Migration failed: {str(J)}"));raise