import ftrack_api
import time

def update_task_status(event):
    entity = event['data'].get('entity')
    if not entity or entity.get('entityType') != 'AssetVersion':
        return

    session = event['source']['session']
    version_id = entity.get('entityId')
    version = session.query(f'AssetVersion where id is {version_id}').first()

    if not version:
        return

    task = version['task']
    if not task:
        return

    version_status = version['status']
    if version_status:
        task['status'] = version_status
        session.commit()
        print(f'Updated task status to {version_status["name"]} for task {task["name"]}')

def main():
    session = ftrack_api.Session(
        server_url='https://secondprize.ftrackapp.com',
        api_key='NTVjM2I1YTgtYjU3Mi00YWM2LThhNWItZDc2MjUwNjhiMGE5Ojo1MjJkNTQxYy05NWM1LTRhMjAtODVhNy1hYzYyNzY1MTJjMWU',
        api_user='second8prize@gmail.com'
    )
    session.event_hub.subscribe('ftrack.update', update_task_status)
    print('Listening to Ftrack...')
    session.event_hub.wait()

if __name__ == '__main__':
    main()
