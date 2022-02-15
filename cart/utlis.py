#va ahacer responsable de crear la sesion y obtener una orden de una seccion
from .models import Orden
def get_or_set_or_session(request):
    orden_id=request.session.get('orden_id',None)
    if orden_id is None:
        orden=Orden()
        orden.save()
        request.session['orden_id']=orden.id
    else:
        try:
            orden=Orden.objects.get(id=orden_id,ordenn=False)    
        except Orden.DoesNotExist:
            orden=Orden()
            orden.save()
            request.session['orden_id']=orden.id
            
    if request.user.is_authenticated and orden is None:
        orden.user=request.user
        orden.save()
    return orden    
