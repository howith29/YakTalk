from medical_rag import MedicalRAGSystem
from intent_analyzer import MedicalChat
from emergency_evaluator import EmergencyEvaluator

from image_processor import ImageProcessor # 추가

class CompleteMedicalChat(MedicalChat):
    def __init__(self, rag_system=None):
        # 기존 MedicalChat 초기화
        super().__init__(rag_system)

        # 응급도 평가
        self.emergency_evaluator = EmergencyEvaluator()

        # 이미지 프로세서 추가
        self.image_processor = ImageProcessor()

    def setup_rag_system(self, csv_path="drug_info.csv", chunk_size=300, chunk_overlap=30):

        # RAG 생성
        self.rag = MedicalRAGSystem()

        try:
            # 데이터 로드
            documents = self.rag.load_csv_data(csv_path)
            # 문서 청크 분할
            split_docs = self.rag.split_documents(chunk_size, chunk_overlap)
            # 임베딩 생성 및 벡터스토어 구축
            vectorstore = self.rag.create_vectorstore(split_docs)


            return True
        
        except Exception as e:
            print(f"RAG System failed: {e}")

    # 이미지 상담 처리
    def process_image_consultation(self, image_file):

        if not self.rag:
            return {
                'success': False,
                'error': 'RAG 시스템이 초기화되지 않았습니다.',
            }
        
        try:
            # 이미지에서 텍스트 추출
            image_result = self.image_processor.processing_image(image_file)

            if not image_result['success']:
                return {
                    'success': False,
                    'error': f"이미지 처리 실패: {image_result['error']}",
                }
            extracted_text = image_result['cleaned_text']
            rag_query = image_result['query']

            print(f"추출된 텍스트: {extracted_text}")

            # 텍스트가 없는 경우
            if not rag_query.strip():
                return {
                    'success': False,
                    'image_analysis': image_result,
                    'consultation_result': None,
                    'final_response': self.generate_no_text_response(),
                    'type': 'no_text_found'
                }
            
            # 추출된 텍스트 전달 
            consultation_result = self.complete_consultation(rag_query)

            # 결과 통합
            if consultation_result.get('success'):
                final_response = self.combine_image_and_consultation(
                    image_result, consultation_result
                )

                return {
                    'success': True,
                    'image_analysis': image_result,
                    'consultation_result': consultation_result,
                    'final_response': final_response,
                    'type': 'image_consultation'
                }
            else:
                return {
                    'sucess': False,
                    'error': f"상담 처리 실패: {consultation_result.get('error', '알 수 없는 오류')}",
                }
            
        except Exception as e:
            print(f"이미지 상담 처리 중 오류 발생: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        
    # 이미지에서 텍스트를 찾지 못했을 때 응답
    def generate_no_text_response(self):

        return """
이미지에서 읽을 수 있는 텍스트를 찾을 수 없습니다.

💡 더 선명한 사진을 위한 팁:
• 밝은 조명에서 촬영하세요
• 약물명이 선명하게 보이도록 가까이에서 촬영
• 흔들림 없이 정면에서 촬영
• 약물 포장지의 글자 부분을 중심으로 촬영

또는 약물명을 직접 텍스트로 입력해주세요!
"""

    # 이미지와 상담 결과 통합
    def combine_image_and_consultation(self, image_result, consultation_result):
        extracted_text = image_result['extracted_text']
        base_response = consultation_result['final_response']

        # 기존 응답에 이미지 정보 추가
        combined_response = f"""
이미지 분석 완료:
{base_response}
이미지에서 인식된 내용: "{extracted_text}"
"""
        return combined_response

    # 완전한 의료 상담 프로세스
    def complete_consultation(self, user_question):

        if not self.rag:
            return {"error":"RAG System failed, Check setup_rag_system()"}

        print("상담 시작")
        print(f"사용자 질문 {user_question}")

        try:
            # 의도 분석
            analysis = self.intent_analyzer.analyze_intent(user_question)

            print("분석 결과:")
            print(f"   - 질문 유형: {analysis['query_type']}")
            print(f"   - 감지된 약물: {analysis['detected_drugs']}")
            print(f"   - 증상: {analysis['symptoms']}")
            print(f"   - 응급 키워드: {analysis['emergency_keywords']}")
            print(f"   - 신뢰도: {analysis['confidence']}")

            # 응급도 평가
            emergency_result = self.emergency_evaluator.evaluate_emergency_level(analysis)

            print("응급도 결과:")
            print(f"   - Level: {emergency_result['level']}")
            print(f"   - 설명: {emergency_result['description']}")
            print(f"   - 조치: {emergency_result['action']}")
            print(f"   - 근거: {emergency_result['reasoning']}")

            # RAG 검색 및 답변 생성
            # 기존 enhanced_query 메소드 재활용
            enhanced_query = self.enhance_query(user_question, analysis)
            print(f"강화된 검색어: {enhanced_query}")

            # 기존 RAG 답변 생성
            rag_result = self.rag.ask_question(user_question, analysis['query_type'])
            base_answer = rag_result['result'] if rag_result else "관련 정보를 찾을 수 없습니다."

            # 최종 응답 생성
            # response_template = self.emergency_evaluator.get_response(emergency_result)
            # final_response = response_template.format(
            #     base_answer=base_answer,
            #     level=emergency_result['level'],
            #     description=emergency_result['description'],
            #     action=emergency_result['action']
            # )
            final_response = self.emergency_evaluator.get_response_by_type(analysis, base_answer, emergency_result)

            # 결과 정리
            result = {
                'success': True,
                'question': user_question,
                'analysis': analysis,
                'emergency': emergency_result,
                'base_answer': base_answer,
                'final_response': final_response,
                'enhanced_query': enhanced_query
            }

            # 최종 응답 출력
            print("최종 응답:")
            print(final_response)

            return result
        
        except Exception as e:
            print(f"처리 중 오류 발생: {e}")
            return {
                'success': False,
                'error': str(e),
                'question': user_question
            }
    
    # 테스트 시나리오!
    def demo_conversation(self):
        demo_questions = [
            "타이레놀 먹고 속이 아파요",
            "해열제 하루에 몇 번 먹어야 하나요?", 
            "두통에 좋은 약 추천해주세요",
            "호흡곤란이 심해서 119 불러야 하나요?",
            "활명수는 언제 먹는 거예요?"
        ]
        
        results = []
        
        for i, question in enumerate(demo_questions, 1):
            print(f"\n\n {i}/{len(demo_questions)}")
            result = self.complete_consultation(question)
            results.append(result)
            
            # 간단한 요약 출력
            if result.get('success'):
                analysis = result['analysis']
                emergency = result['emergency']
                print("\n 요약:")
                print(f"   질문 유형: {analysis['query_type']}")
                print(f"   응급도: Level {emergency['level']} - {emergency['description']}")
                
                if emergency['level'] >= 4:
                    print("높은 응급도 감지! 즉시 대응 필요")
                elif emergency['level'] >= 2:
                    print("주의 필요, 경과 관찰")
                else:
                    print("일반 상담")
        
        print(f"\n 완료, 총 {len(results)}개 질문 처리")
        
        # 전체 통계
        emergency_count = sum(1 for r in results if r.get('success') and r['emergency']['level'] >= 4)
        side_effect_count = sum(1 for r in results if r.get('success') and r['analysis']['query_type'] == 'side_effect')
        
        print(f"\n 테스트 통계:")
        print(f"   - 총 질문: {len(results)}개")
        print(f"   - 부작용 상담: {side_effect_count}개")
        print(f"   - 응급상황 감지: {emergency_count}개")

        # 이미지 기능 테스트
        self.test_image_functionality()
        
        return results
    
    # 단일 질문 테스트
    def quick_test(self, question):
        
        if not self.rag:
            print("RAG 시스템을 먼저 구축해주세요: chatbot.setup_rag_system()")
            return None
        
        print(f" 빠른 테스트: '{question}'")
        result = self.complete_consultation(question)
        
        if result.get('success'):
            print("처리 완료!")
            return result
        else:
            print(f"처리 실패: {result.get('error')}")
            return None
        
    # 이미지 기능 테스트
    def test_image_functionality(self):
        
        from PIL import Image, ImageDraw

        # 테스트용 이미지 생성
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((20, 30), "타이레놀 500mg", fill='black')

        # 임시 파일로 저장
        test_path = 'test_image_integration.png'
        img.save(test_path)

        # 이미지 상담 처리
        result = self.process_image_consultation(test_path)

        if result['success']:
            print("이미지 상담 성공!")
            print(f"응답 타입: {result['type']}")
            if result['type'] == 'image_consultation':
                emergency_level = result['consultation_result']['emergency']['level']
                print(f"응급도: Level {emergency_level}")
            print(f"최종 응답 미리보기:\n{result['final_response'][:200]}...")
        else:
            print(f"이미지 상담 실패: {result['error']}")
        
        # 임시 파일 삭제
        import os
        if os.path.exists(test_path):
            os.remove(test_path)

def main():
    # 쳇봇 초기화
    chat = CompleteMedicalChat()

    # RAG 구축
    success = chat.setup_rag_system('drug_info.csv')

    if not success:
        print("rag 구축 실패")
        return None
    
    # 테스트 실행
    results = chat.demo_conversation()
    
    return chat

def single_test():
    
    print("응급상황 감지 테스트")
    
    chat = CompleteMedicalChat()
    
    if chat.setup_rag_system('drug_info.csv'):
        # 응급상황 테스트
        emergency_question = "타이레놀 먹고 호흡곤란이 심하고 의식이 흐려져요"
        result = chat.quick_test(emergency_question)
        
        if result and result.get('success'):
            level = result['emergency']['level']
            if level >= 4:
                print(f"\n 응급상황 감지 테스트 성공! Level {level}")
            else:
                print(f"\n일반 상담으로 분류됨: Level {level}")
        
        return chat
    else:
        print("시스템 구축 실패")
        return None
    
# 이미지 기능만 단독 테스트
def image_only_test():
    print("이미지 기능 단독 테스트")

    chat = CompleteMedicalChat()
    
    # RAG 시스템 구축
    if chat.setup_rag_system('drug_info.csv'):
        # 이미지 기능 테스트
        chat.test_image_functionality()
    else:
        print("RAG 시스템 구축 실패")
    
    return chat

if __name__ == "__main__":

   #chatbot_system = main()

    
    # chatbot_system = single_test()
    chatbot_system = image_only_test()