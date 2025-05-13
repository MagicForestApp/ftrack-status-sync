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
        server_url='https://yourstudio.ftrackapp.com',
        api_key='XXXXXXXXXXXX',
        api_user='example@example.com'
    )
    session.event_hub.subscribe('ftrack.update', update_task_status)
    print('Listening to Ftrack...')
    session.event_hub.wait()

if __name__ == '__main__':
    main()
