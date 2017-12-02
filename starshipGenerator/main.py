bl_info = {
    "name": "SpaceShipGenerator",
    "category": "Object",
    "location": "View3D > Object >spaceship_start",
    "version": (0, 13)
}


import sys
sys.path.append("C:\work\workBox\BlenderFiles\starshipGenerator")
sys.path.append("/home/nail/workspace/blenderRepo/starshipGenerator")
import pika
import bpy
import generator1

class SpaceShipGenerator(bpy.types.Operator):
    """Generate Ship"""
    bl_idname = "object.space_ship"
    bl_label = "Start Spaceship Generator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        while True:
            try:
                connectToServer()
            except:
                print("CONNECTION ERROR(plugin)")

def register():
    bpy.utils.register_class(SpaceShipGenerator)
    bpy.types.VIEW3D_MT_object.append(menuFunc)
    print("registered")

def unregister():
    bpy.utils.unregister_class(SpaceShipGenerator)
    bpy.types.VIEW3D_MT_object.remove(menuFunc)
    print("unregistered")

def menuFunc(self, context):
    self.layout.operator(SpaceShipGenerator.bl_idname)

def exportMesh():
    ob = bpy.data.objects["hull"]
    ob.select = True
    str3 = "model.obj"
    
    bpy.ops.export_scene.obj(filepath = str3)
    out = open(str3, 'r')
    return out.read()

def connectToServer():
    print("connection --start")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host = "service-queue.cloudapp.net",
            virtual_host = "gshitter",
            credentials = pika.PlainCredentials(
                username = "nail84",
                password = "nail84"
                )
            ,heartbeat_interval = 5
            ,retry_delay = 2
            ,socket_timeout = 2
            ,connection_attempts = 99999
            )
    )
    channel = connection.channel()
    channel.queue_declare(queue='blender.requests')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue='blender.requests')

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
    print("connection --finish")

def on_request(ch, method, props, body):
    print("on_req")
    print(props.reply_to)
    try:
        generator1.main()
        response = exportMesh()
    except:
        response = "error"
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == "__main__":
    # register()
    while True:
        try:
            connectToServer()
        except:
            print("CONNECTION ERROR")
    # testMain()
